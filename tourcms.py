import hmac
import hashlib
import datetime as dt
try:  # Python 3
    import urllib.parse as urllib
except ImportError:
    import urllib
try:  # Python 3
    import urllib.request as urllib2
except ImportError:
    import urllib2
try:
    import xmltodict
except ImportError:
    pass
import dicttoxml
import time
import base64
import logging


__author__ = 'Jonathan Harrington'
__version__ = '0.4'
__license__ = 'BSD'


class Connection(object):
    def __init__(self, marketplace_id, private_key, result_type="raw", loglevel=logging.CRITICAL, channel_id=None):
        try:
            int(marketplace_id)
        except ValueError:
            raise TypeError("Marketplace ID must be an Integer")
        self.marketplace_id = int(marketplace_id)
        if channel_id:
            try:
                int(channel_id)
            except ValueError:
                raise TypeError("Channel ID must be an Integer")
        self.channel_id = int(channel_id) if channel_id else 0
        self.private_key = private_key
        self.result_type = result_type
        self.base_url = "https://api.tourcms.com"
        self.logger = logging.getLogger("tourcms")
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(loglevel)

    def _generate_signature(self, path, verb, channel, outbound_time):
        string_to_sign = u"{0}/{1}/{2}/{3}{4}".format(
            channel, self.marketplace_id, verb, outbound_time, path)
        self.logger.debug("string_to_sign is: {0}".format(string_to_sign))
        dig = hmac.new(self.private_key.encode('utf8'),
                       string_to_sign.encode('utf8'), hashlib.sha256)
        b64 = base64.b64encode(dig.digest())
        return urllib.quote_plus(b64)

    def _response_to_native(self, response):
        try:
            return xmltodict.parse(response)['response']
        except KeyError:
            return xmltodict.parse(response)
        except NameError:
            self.logger.error(
                "XMLtodict not available, install it by running\n\t$ pip install xmltodict\n")
            return response

    def _get_channel(self, channel):
        '''
        Parse the channel id if present or default to the channel id provided on initialisation.
        :returns: The channel id or zero.
        '''
        try:
            return int(channel)
        except:
            return self.channel_id  # defaults to 0

    def _get_url(self, url, channel):
        '''
        Gets the correct /p/ or /c/ route depending on the presence of channel id.
        :url: a url string with format "/{}/route.xml".
        :channel: channel id or None to default to channel id provided on initialisation.
        :returns: the formatted url with 'p' for marketplace agents (no channel), or 'c' for tour operators.
        '''
        channel = self._get_channel(channel)
        return url.format('p' if channel == 0 else 'c')

    def _request(self, path, channel=None, params={}, verb="GET", mlvl=False):
        channel = self._get_channel(channel)
        if params:
            query_string = "?" + urllib.urlencode(params)
        else:
            query_string = ''

        url = self.base_url + path + query_string
        self.logger.debug("url is: {0}".format(url))

        # Generating two different times here as I couldn't figure out how to make one format from the other
        # Previous version broke when running in a non GMT environment
        # Paul (TourCMS)

        # Current unix timestamp, used in the signature
        sign_time = int(time.time())

        # Current UTC time, used in the Date header
        req_time = dt.datetime.utcnow()

        signature = self._generate_signature(
            path + query_string, verb, channel, sign_time
        )
        headers = {
            "Content-type": "text/xml",
            "charset": "utf-8",
            "Date": req_time.strftime("%a, %d %b %Y %H:%M:%S GMT"),
            "Authorization": "TourCMS {0}:{1}:{2}".format(channel, self.marketplace_id, signature)
        }
        self.logger.debug("Headers are: {0}".format(
            ", ".join(["{0} => {1}".format(k, v) for k, v in headers.items()])))

        req = urllib2.Request(url)
        for key, value in headers.items():
            req.add_header(key, value)

        try:
            if verb == "POST":
                if mlvl:
                    data = dicttoxml.dicttoxml(params)
                else:
                    data = urllib.urlencode(params).encode('ascii')
                response = urllib2.urlopen(req, data).read()
            else:
                response = urllib2.urlopen(req).read()
        except urllib2.HTTPError as err:
            print(err)
            return {"error": err.code}

        return response if self.result_type == "raw" else self._response_to_native(response)

    # API Rate Limit Status
    def api_rate_limit_status(self, channel=None):
        return self._request("/api/rate_limit_status.xml", channel)

    # List Channels
    def list_channels(self):
        return self._request("/p/channels/list.xml")

    # Show Channel
    def show_channel(self, channel=None):
        return self._request("/c/channel/show.xml", channel)

    # Search Tours
    def search_tours(self, channel=None, params={}):
        return self._request(self._get_url("/{}/tours/search.xml", channel), channel, params)

    # Search Hotels by specific availability
    def search_hotels_specific(self, tour="", channel=None, params={}):
        params.update({"single_tour_id": tour})
        return self._request("/c/hotels/search-avail.xml", channel, params)

    # List Tours
    def list_tours(self, channel=None, params={}):
        return self._request(self._get_url("/{}/tours/list.xml", channel), channel, params)

    # List Tour Images
    def list_tour_images(self, channel=None, params={}):
        return self._request(self._get_url("/c/tours/images/list.xml", channel), channel, params)

    # Show Tour
    def show_tour(self, tour, channel=None, params={}):
        params.update({"id": tour})
        return self._request("/c/tour/show.xml", channel, params)

    # Show Tour Departures
    def show_tour_departures(self, tour, channel=None, params={}):
        params.update({"id": tour})
        return self._request("/c/tour/datesprices/dep/show.xml", channel, params)

    # Show Supplier (Tour Operator use only)
    def show_supplier(self, supplier_id, channel=None):
        return self._request("/c/supplier/show.xml", channel, {"supplier_id": supplier_id})

    # booking creation > Getting a new booking key (only tour operator)
    def get_booking_redirect_url(self, channel=None, url=''):
        return self._request("/c/booking/new/get_redirect_url.xml", channel, {'url': {'response_url': url}}, "POST")

    # List Tour Locations
    def list_tour_locations(self, channel=None, params={}):
        return self._request(self._get_url("/p/tours/locations.xml", channel), channel, params)

    # List Product Filters (only tour operator)
    def list_product_filters(self, channel=None):
        return self._request("/c/tours/filters.xml", channel)

    # Show Tour Dates & Deals
    def show_tour_dates_deals(self, tour, channel=None, params={}):
        params.update({"id": tour})
        return self._request("/c/tour/datesprices/datesndeals/search.xml", channel, params)

    # Create Customer/Enquiry
    def create_enquiry(self, channel=None, params={}):
        return self._request("/c/enquiry/new.xml", channel, params, "POST")

    # Search Enquiries
    def search_enquiries(self, channel=None, params={}):
        return self._request(self._get_url("/{}/enquiries/search.xml", channel), channel, params)

    # Show Enquiry
    def show_enquiry(self, enquiry, channel=None):
        return self._request("/c/enquiry/show.xml", channel, {'enquiry_id': enquiry})

    def list_payments(self, channel=None):
        return self._request("/c/booking/payment/list.xml", channel)

    def show_booking(self, booking, channel=None):
        response = self._request("/c/booking/show.xml", channel, {'booking_id': booking})
        if type(response) is dict and response.get('error') == "OK" and response.get('booking'):
            b = response['booking']
            b.setdefault('customers', {}).update(customer=filter(None, [b['customers'].get('customer'),]))
            b.setdefault('payments', {}).update(payment=filter(None, [b['payments'].get('payment'),]))
            b.setdefault('custom_fields', {}).update(field=filter(None, [b['custom_fields'].get('field'),]))
        return response

    def show_customer(self, customer, channel=None):
        response = self._request("/c/customer/show.xml", channel, {'customer_id': customer})
        if type(response) is dict and response.get('error') == "OK":
            response.setdefault('customer', {}).setdefault('custom_fields', {}).update(field=filter(None, [response['customer']['custom_fields'].get('field')]))
        return response

    def search_bookings(self, channel=None, params={}):
        response = self._request(self._get_url("/{}/bookings/search.xml", channel), channel, params)
        if type(response) is dict and response.get('error') == "OK":
            response.setdefault('total_bookings_count', '0')
            response.update(booking=filter(None, [response.get('booking'),]))
        return response

    # Agent Search (Tour Operator use only)
    def search_agents(self, channel=None, params={}):
        return self._request("/c/agents/search.xml", channel, params)

    # Check Tour Availability
    def tour_avail(self, tour_id, channel, date, rates):
        params = {
            'id': tour_id,
            'date': date,
        }
        params.update(rates)
        return self._request("/c/tour/datesprices/checkavail.xml", channel, params)

    # Start New Booking
    def start_booking(self, booking_key, customers_no, components, customers, channel=None):
        params = {
            'total_customers': customers_no,
            'booking_key': booking_key,
            'components': components,
            'customers': customers
        }
        return self._request("/c/booking/new/start.xml", channel, params, "POST", True)

    # Commit new booking
    def commit_booking(self, booking_id, channel=None):
        params = {
            'booking_id': booking_id
        }
        return self._request("/c/booking/new/commit.xml", channel, params, "POST", True)

    # add Booking Note
    def booking_note(self, booking_id, note, channel=None, note_type='SERVICE'):
        params = {
            'booking_id': booking_id,
            'note': {
                'type': note_type,
                'text': note
            }
        }
        return self._request("/c/booking/note/new.xml", channel, params, "POST", True)
