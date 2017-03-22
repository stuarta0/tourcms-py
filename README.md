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
*   list\_tours(params, channel)
*   list\_tour\_images(params, channel)
*   show\_tour(params, tour, channel)
*   show\_tour\_departures(params, tour_id, channel)
*   show\_supplier(supplier_id, channel)
*   get\_booking\_redirect\_url(params, channel)
*   list\_tour\_locations(params, channel)
*   list\_product\_filters(channel)
*   show\_tour\_dates\_deals(params, tour_id ,channel)
*   create\_enquiry(params, channel)
*   search\_enquiries(params, channel)
*   show\_enquiry(enquiry_id, channel)

## from the documentation
### api\_rate\_limit\_status(channel)
```
args {
    channel: channel_id
}

response {
    request:	Confirmation of the request,

    error:	Any error message returned (OK),

    remaining_hits:	Number of remaining hits before you are throttled,

    hourly_limit:	Current GET limit per hour,

}
```
### list\_channels()
```
response {
  request:	...,

  error:	...,

  channel: {
    channel_id:	Channel ID,

    account_id:	Account ID,

    channel_name:	Channel name,

    logo_url:	Channel logo URL,

    home_url:	URL website homepage,

    home_url_tracked:	URL website homepage (with agent tracking),

    lang:	Language,

    sale_currency:	Sale currency,

    short_desc:	Short description,

    long_desc:	Long description,

    payment_gateway{
      gateway_id:	,

      name:	name of the gateway, freetext,

      take_visa: 0/1,

      take_mastercard:,

      take_diners:,

      take_discover:,

      take_amex:,

      take_unionpay:,

      gateway_type:	Indicates the type of gateway used,

      *    If the operator is using Spreedly (gateway_type "SPRE")
      spreedly_environment_key:	,

      *    If accessing as a tour operator (not an agent)
      field_(1-10): Configuration settings for the payment gateway,

    }
  }
}
```
### show\_channel(channel)
```
args: {
  channel: channel_id
}

response: {
  request:	...,

  error:	...,

  channel: {
    channel_id:	Channel ID,

    account_id:	Account ID,

    channel_name:	Channel name (Company name),

    get_perm_custbook:	API GET permission - Customers / Bookings,

    get_perm_agsup:	API GET permission - Agents / Suppliers. Permission settings,

    post_perm_custbook:	API POST permission - Customers / Bookings,

    post_perm_agsup:	API POST permission - Agents / Suppliers,

    post_perm_dpa:	API POST permission - Products / Dates / Prices / Availability,

    home_url:	URL website homepage,

    home_url_tracked:	URL website homepage (with agent tracking),

    logo_url:	Channel logo URL,

    lang:	Channel language,

    utc_offset_mins:	Local time: Offset (minutes) from UTC,

    sale_currency:	Sale currency (prices returned in this currency),

    base_currency:	Base currency - for accounting integrations only,

    connection_date:	Date you connected to this channel (YYYY-MM-DD),

    booking_style:	ENQUIRY, QUOTE, BOOKING,

    short_desc:	Short description,

    long_desc:	Long description,

    very_long_desc:	Very long description,

    why_desc:	Why us?,

    bonding_desc:	Bonding / financial protection,

    certification:	e.g. for activity companies could be industry association memberships,

    cancel_policy:	Cancellation policy,

    terms_and_conditions:	Terms and conditions for booking,

    email_customer:	Sales enquiry email address that can be shown to customers IF you are an agent and sending booking notifications to the supplier, send to this address,

    phone_customer:	Sales enquiry telephone number that can be shown to customers,

    office_hours:	Office hours,

    twitter:	Twitter handle (excludes the @),

    tripadvisor:	URL for TripAdvisor entry,

    youtube:	URL for Youtube channel,

    facebook:	URL for Facebook page,

    flickr:	URL for Flickr photo page,

    othersm:	URL for some other social media site (e.g. Ning, blog, forums etc),

    address_1:	Address line 1,

    address_2:	Address line 2,

    address_city:	City,

    address_state:	State,

    address_postcode:	Postcode / Zipcode,

    address_country:	Country code,

    commercial_email_private:	Email address for partners to use to contact the channel,

    commercial_contactname_private:	Name of the channel contact,

    commercial_pitch_private:	What the standard deal for this channel is,

    commercial_ppl_private:	Interested in pay per lead,

    commercial_dir_private:	Interested in directory listings / pay to list,

    commercial_ppc_private:	Interested in pay per click,

    commercial_aff_private:	Interested in affiliate deals (consumer books with channel directly),

    commercial_ag_private:	Interested in agent deals (agent takes money),

    commercial_any_private:	Interested in all sorts of promotional ideas!,

    commercial_avleadtime_private:	Average leadtime (Days between when booking made and start date),

    commercial_avtransaction_private:	Average transaction size (in sale currency),

    commercial_avpeople_private:	Average number of people (pax) in a booking,

    commercial_avclick2book_private:	Average number of unique visitors (via tracking script) to deliver 1 booking,

    commercial_avduration_private:	Average duration of a booking (days) (i.e. whether day tours or longer),

    commercial_percent_online_private:	% bookings received online,

    commercial_percent_convert_private:	% of bookings that ultimately convert to confirmed bookings,

    connection_permission:1 Sell only (No booking access), 2 Summary statistics (For affiliates), 3 Full booking details (Just on own bookings),

    payment_gateway: {...},

    google_analytics_id: Google Analytics ID
  }
}
```
### search\_tours(params, channel)
```
args: {
  channel: channel_id,

  params: {    
    tour_id: tour_id=10 (Tour ID 10 only) Only works if searching in a specific Channel,

    not_tour_id: tour_id=10,12,15 (Tour IDs 10, 12 and 15 only) Only works if searching in a specific Channel,

    channel_id_tour_id: channel_id_tour_id=10_8 (Tour ID 8, from Channel ID 10 only),

    not_channel_id_tour_id: channel_id_tour_id=10_8,10_100,10_101 (Tour IDs 8, 100, 101 only, from Channel ID 10 only),

    booking_style:	Set to booking to only return Tours from Channels (Operators) that take confirmed online bookings (e.g. will ignore Tours from any Channels who take online "bookings" as an Enquiry or Quotation stage of the process),

    k:	Keyword - matches against Tour name, Location, Short description, Summary, Tour code,

    k2:	Keyword #2 (When used with k will be OR),

    k3:	Keyword #3 (When used with k and k2 will be OR),

    k_type:	Set k_type=AND to make k, k2, k3 work as an AND (default is OR),

    location:	Search by "Primary location" text field (Part matches permitted),

    lat:	Latitude of search point,

    long:	Longitude of search point,

    geo_type:	Set to end to search tour end point. By default will search tour start point,

    geo_unit:	Set to km to set unit for proximity search to kilometres. By default will be miles,

    geo_distance:	Define distance for proximity search. Default 50,

    has_sale:	By default will only return tours that have at least one bookable date in the future. Set to all to return all tours,

    has_offer: Set to 1 to return just tours with special offers / deals available.,

    has_sale_month: e.g. has_sale_month=1,2 to return products with something on sale EITHER in January OR February. Can be multiple or just a single month. Use this to create a basic availability search,

    404_tour_url: **error** - Return just those tours that are returning errors **all** - Return all tours,

    start_date: Check availability on a specific date, date format YYYY-MM-DD
    start_date_start: Check availability on a range of start dates, date format YYYY-MM-DD,

    start_date_end: ...,

    between_date_start: start date is after between_date_start and end date is before between_date_end, date format YYYY-MM-DD.,

    between_date_end: ...,

    duration_min: Search by tour duration (Days)و
    duration_max: ...,

    price_range_min: Minimum "From" price. Defaults to USD.,

    price_range_max: Maximum "From" price. Defaults to USD.,

    price_range_currency: defaults to USD. TourCMS will return prices in their original currency, actual ranges may vary slightly,

    min_priority: Minimum, Medium or High priority tours.,

    country: Search by country - two letter ISO country code,

    not_country: EXCLUDE results featuring this country - two letter ISO country code,

    not_accom: Set to 1 to EXCLUDE tour that include accommodation (Product types 1 & 3),

    accom: Set to 1 to ONLY RETURN products that include accommodation (Product types 1 & 3),

    accomrating: e.g. accomrating=4,5,

    product_type: Search by product type - comma separated list e.g. product_type=1,3. http://www.tourcms.com/support/api/mp/tour_search.php#product_type.
    grade: Search by grade - comma separated list e.g. to just search for extreme/challenging products search for grade=4,5,

    tourleader_type: Search by tour leader type - comma separated list e.g. tourleader_type=2,

    suitable_for_solo: 0/1,

    suitable_for_couples: 0/1,

    suitable_for_children: 0/1,

    suitable_for_groups: 0/1,

    suitable_for_students: 0/1,

    suitable_for_business: 0/1,

    suitable_for_wheelchairs: 0/1,

    currency: (USD / EUR / GBP etc),

    lang: Language that the tour description is loaded in e.g. en,

    lang_spoken: Languages spoken on the tour.,

    video_service: Optionally search for only tours that have a video, **all** , **vimeo**, **youtube**.,

    order: **Default order**,**Alphabetical**,**Commercial priority [Default]**,**Departure date**,**Display points**,**Duration**,**Price**,**Special offer**,**Tour creation date**
    qc: Enable/disable "Quality control".
    per_page: Number of results to return per page. Default is 75. Max is 200,

    page: Integer for which page number to return. Default is page 1,

    #### If API called by Tour Operator (not Marketplace Agent)

    category: category=Rafting,

    ANDcategory: ANDcategory=Rafting|Hiking,

    ORcategory: ORcategory=Rafting|Hiking,

    NOTcategory: NOTcategory,

  }
}

response: {
  request:	...,

  error:	...,

  total_tour_count: ,

  tour: {
    channel_id:	Channel ID,

    account_id:	Account ID,

    tour_id:	Tour ID,

    has_sale:	0/1,

    has_d:	0/1,

    has_f:	0/1,

    has_h:	0/1,

    next_bookable_date:	First date the tour is bookable, date format YYYY-MM-DD,

    next_bookable_date_norange:	First date the tour is bookable, date format YYYY-MM-DD,

    last_bookable_date:	Last date the tour is bookable, date format YYYY-MM-DD,

    has_sale_jan:,

    has_sale_feb:,

    has_sale_mar:,

    has_sale_apr:,

    has_sale_may:,

    has_sale_jun:,

    has_sale_jul:,

    has_sale_aug:,

    has_sale_sep:,

    has_sale_oct:,

    has_sale_nov:,

    has_sale_dec:	0/1,,

    tour_code:	Tour code (only returned if set),

    from_price:	Lead in price,

    from_price_display:	Lead in price - html,,

    from_price_unit:	0 - per person (default), 1 - per couple, 2 - per vehicle, 3 - per room,

    from_price_jan:,

    from_price_feb:,

    from_price_mar:,

    from_price_apr:,

    from_price_may:,

    from_price_jun:,

    from_price_jul:,

    from_price_aug:,

    from_price_sep:,

    from_price_oct:,

    from_price_nov:,

    from_price_dec:	Lead in price by the month,,

    sale_currency:	Sale currency (for the lead in price). Currency is set by channel,

    priority:	HIGH, MEDIUM, LOW - Commercial priority,

    thumbnail_image:	The URL for an image to display for this Tour,

    video: {
      video_service:	Video service used to host the video.,

      video_id:	Service-specific ID for the video (if any),

      video_url:	URL to a web page containing the video,

    }
    geocode_start:	Lat,Long geocode for start point,

    geocode_end:	Lat,Long geocode for end point,

    distance:	IF a proximity search, the distance from the search point. Default is miles,

    tour_name:	Tour name - Short,

    tour_name_long:	Tour name - Long,

    start_time:	Start time for the Tour.,

    end_time:	End time for the Tour.,

    country:	List of countries the tour takes place - 2 digit ISO code format, comma separated,

    duration:	Duration (Days),

    duration_desc:	Text description for duration (e.g. 1 week) ,

    location:	Primary location - Perhaps a city name, national park name or region,

    summary:	Summary - Includes primary activity if not clear from tour name,

    shortdesc:	Short description (NO HTML),

    available:	Text description for when available (e.g. March to September),

    tour_url:	URL for the tour detail page,

    tour_url_tracked:	URL for the tour detail page - via agent tracking mechanism,

    book_url:	URL to booking engine / live availability display (can be iframed onto your site),

    tourleader_type:	1 - Tour guide / driver, 2 - Independent / self drive, 3 - Not applicable (e.g. accommodation / event),

    grade:	1 - All ages / Not applicable, 2 - Moderate, 3 - Fit, 4 - Challenging, 5 - Extreme,

    accomrating:	1 - No accommodation / Not applicable, 2 - Luxury, 3 - Moderate, 4 - Comfortable, 5 - Basic, 6 - Various levels,

    product_type:	1 - Accommodation (hotel/campsite/villa/ski chalet/lodge), 2 - Transport/Transfer, 3 - Tour/cruise including overnight stay, 4 - Day tour/trip/activity/attraction (No overnight stay), 5 - Tailor made, 6 - Event, 7 - Training/education, 8 - Other, 9 - Restaurant / Meal alternative
      In the case of "2" (Transport/Transfer).
      0 - Other / not set
      1 - Airport to City
      2 - City to Airport
      3 - Two way return,

    pickup_on_request:	1 - Customer can provide a freetext pickup point, 0 - Customer cannot provide a freetext pickup point,

    pickup_scheduled:	0/1,

    suitable_for_solo: 0/1,

    suitable_for_couples: 0/1,

    suitable_for_children: 0/1,

    suitable_for_groups: 0/1,

    suitable_for_students: 0/1,

    suitable_for_business: 0/1,

    suitable_for_wheelchairs: 0/1,

    languages_spoken:	Languages spoken on the tour. Comma separated list. E.g. "en,pt" for English & Portuguese,

    supplier_id:,

    channel: {
      channel_name:	Channel name (Company name),

      logo_url:	Channel logo URL,

      lang:	Channel language.,

      home_url:	URL website homepage,

      home_url_tracked:	URL website homepage (with agent tracking),

    soonest_special_offer: {
      start_date:,

      end_date:,

      start_time:,

      end_time:,

      date_code:	This is the "Departure code" from a Tour Operators perspective, may be empty,

      note:	Product note,

      min_booking_size:	,

      spaces_remaining:	Number of people that can still book for this date. Generally numeric however could contain the text UNLIMITED,

      special_offer_type:	Type of special offer / deal on this date, 1 - Date specific special price, 2 - Late booking discount, 3 - Early booking discount, 4 - Duration specific discount,

      price_1:	Price for 1 person,

      price_1_display:,

      price_2:	Price,

      price_2_display:,

      special_offer_datetime:	,

      special_offer_note:	,

      original_price_1:	,

      original_price_1_display:,

      original_price_2:,

      original_price_2_display:,

    }
    recent_special_offer: {  
      start_date: ,

      end_date: ,

      start_time: ,

      end_time: ,

      date_code: ,

      note: ,

      min_booking_size: ,

      spaces_remaining: ,

      special_offer_type: ,

      price_1: ,

      price_1_display: ,

      price_2: ,

      price_2_display: ,

      special_offer_datetime: ,

      special_offer_note: ,

      original_price_1: ,

      original_price_1_display: ,

      original_price_2: ,

      original_price_2_display,

    }
    dates_public_bookable: {
      date:
    }
    dates_has_offer: {
      date:
    }
    #### If API called by Tour Operator (not Marketplace Agent)
    custom(1-2):
    }
  }
}
```
### search\_hotels\_specific(params, tour_id, channel)
```
args: {
  channel: , optional

  tour_id: , optional

  params: {
    startdate_yyyymmdd: (YYYY-MM-DD) - Start (check in) date,

    hdur: Duration (days / nights),

    ad: Adults (non mandatory),

    ch: Children (non mandatory),
  }
}

response: [{
  room_rate: {
    label:	Room/Rate name,

    ror:	Room or rate. Rooms have availability control on, rates don't,

    request_start_date:	Start date for request,

    request_end_date:	End date for request,

    request_duration:	Duration (days / nights) in request. Makes it easy to add to the book link,

    request_adults:	Adults requested (or the defaults used if not originally supplied in the request),

    request_children:	Children requested (or the defaults used if not originally supplied in the request),

    whole_chalet:	1 if booking an entire ski chalet, 0 if not (and booking an individual room in a chalet),

    max_adults:	Capacity,

    max_children:	Capacity,

    rooms_remaining:	Number of rooms of the same type that remain available,

    board_basis: {
      code:	Board Basis code,

      name:	Board Basis name,

      price:	Price,

      price_display:	Price with currency symbol / description,

    }
  }
}]
```
### list\_tours(params, channel)
```
args: {
  channel: , optional

  params: {
    booking_style: ...,

    qc: ...,
  }
}

response: {
  request:	...,

  error:	...,

  tour: {
    channel_id: ,

    account_id: ,

    tour_id: ,

    has_sale: ,

    has_d: Departure,

    has_f: freesale,

    has_h: hotel,

    descriptions_last_updated: date,

    tour_name: ,

    supplier_id: ,

    supplier_tour_code: If a Tour Operator is using the API call directly then supplier_tour_code will contain the supplier set tour code. This field is ideal if you are syncronising TourCMS with an external reservation system as this could be the external reservation system tour ID. Not returned when a Marketplace Agent is using the API.,

  }
}
```
### list\_tour\_images(params, channel)
```
args: {
  channel: , optional

  params: { (optional)
    booking_style: ,

    qc: ,
  }
}

response: {
  request:	...,

  error:	...,

  tour: {
    channel_id: ,

    account_id: ,

    tour_id: ,

    images: [{
      image: {
        url_thumbnail: ,

        url: ,

        url_large: ,

        url_xlarge: ,

        url_original: ,
      }
    }]
  }
}

```
### show\_tour(params, tour, channel)
```
args: {
  channel: , optional

  tour: id,

  params: { (optional leave empty object)
    show_options: ,

    show_offers: ,

    order: ...,
  }
}

response: {
  request:	...,

  error:	...,

  tour: {
    channel_id: ,
    account_id: ,
    tour_id: ,
    tour_name: ,
    tour_name_long: ,
    tour_code: ,
    quantity_rule: ,
    from_price: ,
    from_price_display: ,
    from_price_unit: ,
    sale_currency: ,
    has_sale: ,
    has_d: ,
    has_f: ,
    has_h: ,
    created_date: ,
    descriptions_last_updated: ,
    min_booking_size: ,
    max_booking_size: ,
    next_bookable_date: ,
    last_bookable_date: ,
    has_sale_jan: ,
    has_sale_feb: ,
    has_sale_mar: ,
    has_sale_apr: ,
    has_sale_may: ,
    has_sale_jun: ,
    has_sale_jul: ,
    has_sale_aug: ,
    has_sale_sep: ,
    has_sale_oct: ,
    has_sale_nov: ,
    has_sale_dec: ,
    from_price_jan: ,
    from_price_jan_display: ,
    from_price_feb: ,
    from_price_feb_display: ,
    from_price_mar: ,
    from_price_mar_display: ,
    from_price_apr: ,
    from_price_apr_display: ,
    from_price_may: ,
    from_price_may_display: ,
    from_price_jun: ,
    from_price_jun_display: ,
    from_price_jul: ,
    from_price_jul_display: ,
    from_price_aug: ,
    from_price_aug_display: ,
    from_price_sep: ,
    from_price_sep_display: ,
    from_price_oct: ,
    from_price_oct_display: ,
    from_price_nov: ,
    from_price_nov_display: ,
    from_price_dec: ,
    from_price_dec_display: ,
    priority: ,
    country: ,
    geocode_start: ,
    geocode_end: ,
    product_type: ,
    tourleader_type: ,
    grade: ,
    accomrating: ,
    location: ,
    summary: ,
    shortdesc: ,
    longdesc: ,
    itinerary: ,
    duration_desc: ,
    duration: ,
    available: ,
    pick: ,
    inc_ex: ,
    inc: ,
    ex: ,
    tour_url: ,
    tour_url_tracked: ,
    book_url: ,
    suitable_for_solo: ,
    suitable_for_couples: ,
    suitable_for_children: ,
    suitable_for_groups: ,
    suitable_for_students: ,
    suitable_for_business: ,
    suitable_for_wheelchairs: ,
    pickup_on_request: ,
    alternative_tours: {
      tour: [
        {
          tour_id: ,
          tour_name: ,
          tour_name_long: ,
          location: ,
          tour_url: ,
          tour_url_tracked: ,
          book_url: ,
          tour_code: ,
          from_price: ,
          from_price_display: ,
          from_price_unit: ,
          thumbnail_image: ,
          product_type:
        },
        {
          tour_id: ,
          tour_name: ,
          tour_name_long: ,
          location: ,
          tour_url: ,
          tour_url_tracked: ,
          book_url: ,
          tour_code: ,
          from_price: ,
          from_price_display: ,
          from_price_unit: ,
          thumbnail_image: ,
          product_type:
        }
      ]
    },
    images: {
      image: [
        {
          -thumbnail: ,
          url: ,
          image_desc:
        },
        {
          url: ,
          image_desc:
        },
        {
          url: ,
          image_desc:
        },
        {
          url: ,
          image_desc:
        },
        {
          url: ,
          image_desc:
        },
        {
          url: ,
          image_desc:
        }
      ]
    },
    new_booking: {
      people_selection: {
        rate: {
          label_1: ,
          minimum: ,
          maximum: ,
          rate_id: ,
          agecat: ,
          from_price: ,
          from_price_display:
        }
      },
      date_selection: { :  }
    },
    distribution_identifier:
  }
}
```
### show\_tour\_departures(params, tour_id, channel)
```
args: {
  tour_id: ,

  channel: , optional

  params: { (optional)
    start_date_start,

    start_date_end,

    show_closed_departures,

    per_page,

    page,

  }
}

response: {
  request:	...,

  error:	...,

  tour: {
    channel_id: ,

    account_id: ,

    tour_id: ,

    min_booking_size: ,

    max_booking_size: ,

    sale_currency	Sale: ,

    dates_and_prices: {
      total_departure_count: ,

      departure: {        
        departure_id: ,

        code: ,

        start_time: ,

        end_time: ,

        start_date: ,

        end_date: ,

        note: ,

        spaces_remaining: ,

        supplier_note: ,

        guide_language: ,

        status: ,

        book_url: ,

        main_price: {          
          rate_id: ,

          rate_name: ,

          rate_price: ,

          rate_price_display: ,

          is_offer: ,

          date_offer_created: ,

          offer_note: ,

          previous_price: ,

          previous_price_display: ,

          net_price: ,

          agecat: ,

          agerange_min: ,

          agerange_max: ,

          rate_code: ,

        }

        extra_rates: {          
          rate_id: ,

          rate_name: ,

          rate_price: ,

          rate_price_display: ,

          net_price: ,

          agecat: ,

          agerange_min: ,

          agerange_max: ,

          rate_code: ,

        }
      }
    }
  }
}
```
### show\_supplier(supplier_id, channel)
```
args: {
  channel: ,

  supplier_id: ,
}

response: {
  request:	...,

  error:	...,

  supplier: {
    supplier_id: ,

    channel_id: ,

    account_id: ,

    name: ,

    code: ,

    home_url: ,

    logo_url: ,

    contact_name: ,

    email_bookings: ,

    email_accounts: ,

    address: ,

    short_desc: ,

    long_desc: ,

    why_desc: ,

    bonding_desc: ,

    certification: ,

    cancel_policy: ,

    terms_and_conditions: ,

  }
}
```
### get\_booking\_redirect\_url(params, channel)
```
args: {
  channel: ,
  params: {
    url: {
      response_url: This is the URL that you would like TourCMS to return the customer to. This will likely be a page hosted on your website that represents the next step of the booking process.

    }
  }
}

response: {
  request:	...,

  error:	...,

  url: {
    redirect_url: This is the URL that TourCMS requires you to send the customer to before you can start building their booking. TourCMS will do it's thing and then redirect the customer to the response_url you posted in your initial request.

  }
}
```
### list\_tour\_locations(params, channel)
```
args: {
  channel: ,

  params: {
    lang: ,

    booking_style: ,

    qc: ,

  }
}

response: {
  request: ...,

  error: ...,

  unique_location: {
    location: ,

    country_code: ,

    country_name: ,
  }
}
```
### list\_product\_filters(channel)
```
args: {
  channel: ,
}

response: {
  request: ...,

  error: ...,

  filters: {
    filter: {
      filter_id: ,

      filter_name: ,

      tour: {
        tour_id: ,

        tour_name: ,

        tour_code: ,
      }
    }
  }
}
```
### show\_tour\_dates\_deals(params, tour_id ,channel)
```
args: {
  channel: ,

  tour_id: ,

  params: {
    startdate_start: ,

    startdate_end: ,

    between_date_start: ,

    between_date_end: ,

    has_offer: ,

    order: ,

    distinct_start_dates: Set to 1 to only return one entry per date, this is useful when building an availability calendar or similar where the only desired information is a list of dates which have some form of availability on them,

  }
}

response: {
  request: ...,

  error: ...,

  total_date_count: ,

  channel_id: ,

  account_id: ,

  tour_id: ,

  dates_and_prices: {    
    start_date: ,

    end_date: ,

    start_time: ,

    end_time: ,

    date_code: ,

    note: ,

    guide_language: {
      language: ,

    },

    sale_currency: ,

    min_booking_size: ,

    spaces_remaining: ,

    special_offer_type: ,

    status: ,

    book_url: ,

    price_1: ,

    price_1_display: ,

    price_2: ,

    price_2_display: ,

    ### If special_offer_type is not 0

    special_offer_datetime: ,

    special_offer_note: ,

    original_price_1: ,

    original_price_1_display: ,

    original_price_2: ,

    original_price_2_display: ,

  }
}
```
### create\_enquiry(params, channel)
```
args: {
  channel: ,

  params: {
    enquiry: {
      customer_id: ,

      title: ,

      firstname: ,

      surname: ,

      email: ,

      tel_home: ,

      address: ,

      city: ,

      county: ,

      postcode: ,

      country: ,

      enquiry_detail: ,

      ### Less commonly used fields

      enquiry_type: ,

      enquiry_category: ,

      enquiry_assignto: ,

      enquiry_value: ,

      enquiry_outcome: ,

      enquiry_followup_date: ,

      middlename: ,

      nationality: ,

      gender: ,

      dob: ,

      agecat: ,

      pass_num: ,

      pass_issue: ,

      pass_issue_date: ,

      pass_expiry_date: ,

      wherehear: ,

      fax: ,

      tel_work: ,

      tel_mobile: ,

      tel_sms: ,

      contact_note: ,

      diet: ,

      medical: ,

      nok_name: ,

      nok_relationship: ,

      nok_tel: ,

      nok_contact: ,

    }
  }
}

response: {
  request: ...,

  error: ...,

  enquiry: {
    channel_id: ,

    accound_id: ,

    enquiry_id: ,

    customer_id: ,
  }
}
```
### search\_enquiries(params, channel)
```
args: {
  channel: ,

  params: {
    made_date_start: ,

    made_date_end: ,

    unique: ,

    customer_id: ,

    per_page: ,

    page: ,

  }
}

response: {
  request: ...,

  error: ...,

  enquiry: {
    channel_id: ,

    account_id: ,

    enquiry_id: ,

    customer_id: ,

    made_date_time: ,

    status: ,

    status_text: ,

    type: ,

    category: ,

    detail: ,

    value: ,

    outcome: ,

    followup_date: ,

    closed_date_time: ,

  }

  total_enquiries_count: ,
}
```
### show\_enquiry(enquiry_id, channel)
```
args: {
  channel: ,

  enquiry_id: ,
}

response: {
  request: ...,

  error: ...,

  enquiry: {
    channel_id: ,

    account_id: ,

    enquiry_id: ,

    customer_id: ,

    made_date_time: ,

    status: 0 = "Triage" (default initial status), 1 = "Open (Staff)", 2 = "Open (Customer)", 3 = "Open (Agent)", 4 = "Open (Supplier)", 5 = "Closed / Solved (Success / Booked)", 6 = "Solved (Failure / Not Booked)",

    status_text: ,

    type: ,

    category: ,

    detail: ,

    value: ,

    outcome: ,

    followup_date: ,

    closed_date_time: ,

  }
}
```

## Dependencies

None. xmltodict optional. Tested with Python 2.6, 2.7, 3.3 & 3.6.

## Copyright

Copyright (c) 2012 Jonathan Harrington. See LICENSE.txt for further details.
