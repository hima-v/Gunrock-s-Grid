# config.py
# just has all the constants and stuff we reuse across files
# easier to change things in one place instead of hunting thru every file

# ---- Memorial Union coordinates (our reference point for distance calc) ----
# got these from google maps, right clicked on the MU building
MU_LAT = 38.5424
MU_LON = -121.7483

# radius in miles for transit score
# basically how far from the apartment we look for bus stops
TRANSIT_RADIUS_MILES = 0.25

# database file name
DB_NAME = "davis_housing.db"

# how many seconds to wait between requests so we dont get blocked
# craigslist is chill but we still dont want to hammer them
SCRAPE_DELAY_MIN = 1.5
SCRAPE_DELAY_MAX = 3.0

# neighborhoood boundaries
# v2 - expanded ranges and removed gaps between neighborhoods
# drew these on google maps, checked against known apartment complexes
# i-80 runs east-west at about 38.555, covell blvd at ~38.560
# russell blvd goes east-west thru campus at about 38.545
# downtown is the compact grid between 1st-5th st and A-L st
NEIGHBORHOOD_BOUNDS = {
    "Downtown": {
        "lat_min": 38.540,
        "lat_max": 38.552,
        "lon_min": -121.755,
        "lon_max": -121.730,
    },
    "North Davis": {
        "lat_min": 38.552,
        "lat_max": 38.580,
        "lon_min": -121.775,
        "lon_max": -121.720,
    },
    "South Davis": {
        "lat_min": 38.520,
        "lat_max": 38.540,
        "lon_min": -121.775,
        "lon_max": -121.720,
    },
    "East Davis": {
        "lat_min": 38.535,
        "lat_max": 38.565,
        "lon_min": -121.720,
        "lon_max": -121.690,
    },
    "West Davis": {
        "lat_min": 38.535,
        "lat_max": 38.565,
        "lon_min": -121.800,
        "lon_max": -121.755,
    },
}

# craigslist base url for davis apartments (under sacramento region)
CRAIGSLIST_URL = "https://sacramento.craigslist.org/search/davis-ca/apa"

# max search result pages to scrape (each page has ~120 listings)
MAX_PAGES = 3

# user agent so we look like a normal browser
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
