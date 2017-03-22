# tourcms

A simple wrapper for connecting to [TourCMS Marketplace API](http://www.tourcms.com/support/api/mp/). This wrapper mirrors the TourCMS PHP library.

[![Build Status](https://travis-ci.org/prio/tourcms.png?branch=master)](https://travis-ci.org/prio/tourcms)

## Install

NOTE: At the time of writing this repo is ahead of the version in pip which does not include the fix for non GMT environments.

    pip install tourcms

## Usage

Using the library is as simple as creating a **Connection** object:

    conn = tourcms.Connection(marketplace_id, private_key, result_type)

Your Marketplace ID and Private Key can be found in the TourCMS Partner Portal. The result type can be one of **dict** or **raw** where **raw** will return the raw XML from the API and **dict** will return a dictionary of the result. Dict requires xmltodict to be installed.

### Working with your connection in Raw mode

```python
    # Instantiate the connection
    import os
    from tourcms import Connection

    conn = Connection(0, os.getenv('TOURCMS_PRIVATE_KEY'))

    # Check we're working
    conn.api_rate_limit_status(channel_id)
    => "<?xml version="1.0" encoding="utf-8" ?><response><request>GET /api/rate_limit_status.xml</request>
        <error>OK</error><remaining_hits>1999</remaining_hits><hourly_limit>2000</hourly_limit></response>"

    # List the channels we have access to
    conn.list_channels(channel_id)
    => ""<?xml version="1.0" encoding="utf-8" ?><response><request>GET /p/channels/list.xml</request>
        <error>OK</error><channel>(...)</channel><channel>(...)</channel><channel>(...)</channel></response>"

    # Show a particular channel
    conn.show_channel(1234567)
    => ""<?xml version="1.0" encoding="utf-8" ?><response><request>GET /p/channels/list.xml</request>
        <error>OK</error><channel>(...)</channel></response>"
```

### Working with your connection in Dictionary mode
Requires xmltodict to be installed

    pip install xmltodict


```python
    # Instantiate the connection
    conn = Connection(0, os.getenv('TOURCMS_PRIVATE_KEY'), "dict")

    # Check we're working
    conn.api_rate_limit_status(channel_id)
    => OrderedDict([(u'request', u'GET /api/rate_limit_status.xml?'), (u'error', u'OK'), (u'remaining_hits', u'1999'), (u'hourly_limit', u'2000')])
    obj["hourly_limit"]
    => 2000   
```

### Passing parameters

Many TourCMS methods accept parameters. Most methods take a dictionary of parameters like so:

    obj = conn.search_tours({"country": "GB", "lang": "en"})

## List of functions in tourcms.Connection

*   api\_rate\_limit\_status(channel)
*   list\_channels()
*   show\_channel(channel)
*   search\_tours(params, channel)
*   search\_hotels\_specific(params, tour_id, channel)
*   list\_tours(channel)
*   list\_tour\_images(channel)
*   show\_tour(tour, channel)
*   show\_tour\_departures(tour_id, channel)
*   show\_supplier(supplier_id, channel)
*   get\_booking\_redirect\_url(params, channel)
*   list\_tour\_locations(channel)
*   list\_product\_filters(channel)
*   show\_tour\_dates\_deals(params, tour_id ,channel)
*   create\_enquiry(params, channel)
*   search\_enquiries(params, channel)
*   show\_enquiry(enquiry_id, channel)

## from the documentation
### api\_rate\_limit\_status(channel)
args {
  channel: channel_id
}
response {
  request:	Confirmation of the request that you sent,
  error:	Any error message returned, if there is no error this will just contain the text OK,
  remaining_hits:	Number of remaining hits before you are throttled,
  hourly_limit:	Current GET limit per hour,
}

### list\_channels()
response {
  request:	Confirmation of the request that you sent,
  error:	Any error message returned, if there is no error this will just contain the text OK,
  channel:  channel_id:	Channel ID,
            account_id:	Account ID,
            channel_name:	Channel name,
            logo_url:	Channel logo URL,
            home_url:	URL website homepage,
            home_url_tracked:	URL website homepage (with agent tracking),
            lang:	Language,
            sale_currency:	Sale currency,
            short_desc:	Short description,
            long_desc:	Long description,
            payment_gateway:  gateway_id:	TourCMS unique identifier for this gateway,
                              name:	Staff entered name for the gateway, freetext
                              take_visa: A field for each possible supported credit/debit card type (MasterCard, Diners Club, Discover, American Express, UnionPay). Will be "1" if card type is accepted, "0" if it isn't
                              take_mastercard:
                              take_diners:
                              take_discover:
                              take_amex:
                              take_unionpay:
                              gateway_type:	Indicates the type of gateway used, if "SPRE" then the operator is using Spreedly which allows agents websites/apps to offer payments direct to the operator. Other values include "PAYP" for PayPal, "AUN" for Authorize.net
                              #### If the operator is using Spreedly (gateway_type "SPRE")
                              spreedly_environment_key:	Required for taking credit card payments via Spreedly payment solution powered companies. This is open for travel agent use as well as supplier. More details
                              #### If accessing as a tour operator (not an agent)
                              field_(1-10): Configuration settings for the payment gateway, useful if building a custom booking engine, allows gateway details to be stored once - in TourCMS.10 fields, not all are used for all gateways (so some may be blank). The data stored in each numbered field varies by gateway, see the gateway settings page in TourCMS to match up the correct fields.
}

## Dependencies

None. xmltodict optional. Tested with Python 2.6, 2.7, 3.3 & 3.6.

## Copyright

Copyright (c) 2012 Jonathan Harrington. See LICENSE.txt for further details.
