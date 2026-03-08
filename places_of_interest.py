# places_of_interest.py
# database of important places in davis that students care about
# we compute distance from each listing to each of these places
# this gives us way more useful proximity data than just "distance to MU"
#
# all coordinates were verified by looking up each place on google maps
# and cross-checking with the actual address

import pandas as pd
import os
import sys
from math import radians, sin, cos, sqrt, atan2


# ---- Points of Interest ----
# each entry has: name, lat, lon, category
# categories help us group them for analysis (campus, grocery, social, transit)
# coords sourced from google maps / google places API

PLACES_OF_INTEREST = [
    # --- campus buildings ---
    {
        "name": "Memorial Union (MU)",
        "lat": 38.5423,
        "lon": -121.7496,
        "category": "campus",
        "description": "main student union building, center of campus life"
    },
    {
        "name": "Silo",
        "lat": 38.5382,
        "lon": -121.7527,
        "category": "campus",
        "description": "food court area between classes, south side of campus"
    },
    {
        "name": "Shields Library",
        "lat": 38.5397,
        "lon": -121.7495,
        "category": "campus",
        "description": "main library - where everyone studies"
    },
    {
        "name": "ARC (Activities & Recreation Center)",
        "lat": 38.5428,
        "lon": -121.7591,
        "category": "campus",
        "description": "gym / rec center on west side of campus"
    },
    {
        "name": "Student Health Center",
        "lat": 38.5427,
        "lon": -121.7615,
        "category": "campus",
        "description": "health and counseling services"
    },

    # --- grocery stores ---
    {
        "name": "Trader Joes",
        "lat": 38.5467,
        "lon": -121.7615,
        "category": "grocery",
        "description": "885 Russell Blvd - closest TJs to campus"
    },
    {
        "name": "Safeway (North)",
        "lat": 38.5621,
        "lon": -121.7663,
        "category": "grocery",
        "description": "1451 W Covell Blvd - north davis safeway"
    },
    {
        "name": "Nugget Markets (East Covell)",
        "lat": 38.5610,
        "lon": -121.7331,
        "category": "grocery",
        "description": "1414 E Covell Blvd - nicer grocery store, bit pricey"
    },
    {
        "name": "Davis Food Co-op",
        "lat": 38.5493,
        "lon": -121.7399,
        "category": "grocery",
        "description": "620 G St - organic/local grocery downtown"
    },
    {
        "name": "Target",
        "lat": 38.5543,
        "lon": -121.6997,
        "category": "grocery",
        "description": "4601 2nd St - east davis, only target in town"
    },

    # --- social / food / fun ---
    {
        "name": "Downtown Davis (3rd & G St)",
        "lat": 38.5448,
        "lon": -121.7389,
        "category": "social",
        "description": "heart of downtown - restaurants, bars, woodstocks pizza"
    },
    {
        "name": "Davis Farmers Market",
        "lat": 38.5447,
        "lon": -121.7440,
        "category": "social",
        "description": "central park - sat mornings and wed afternoons"
    },

    # --- transit ---
    {
        "name": "Davis Amtrak Station",
        "lat": 38.5435,
        "lon": -121.7377,
        "category": "transit",
        "description": "train station downtown - capitol corridor to sac/bay"
    },
]


def haversine_miles(lat1, lon1, lat2, lon2):
    """distance between two points on earth in miles
    same formula as in enrich.py but we keep a copy here
    so this file can run standalone without importing enrich
    """
    R = 3958.8
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def compute_all_distances(df):
    """for each listing, compute distance to every POI
    
    adds new columns to the dataframe like:
      dist_to_memorial_union_mu
      dist_to_silo
      dist_to_trader_joes
      etc.
    
    also adds:
      nearest_grocery (name of closest grocery store)
      nearest_grocery_dist (distance in miles)
      nearest_campus (name of closest campus building)
      nearest_campus_dist (distance in miles)
    
    this is more useful than just one distance metric bc students
    care about different things - some want to be near the gym,
    others near grocery stores, others near downtown bars lol
    """
    print(f"computing distances to {len(PLACES_OF_INTEREST)} points of interest...")
    
    # compute distance to each POI
    for poi in PLACES_OF_INTEREST:
        # make a clean column name from the place name
        # eg "Memorial Union (MU)" -> "dist_to_memorial_union_mu"
        col_name = "dist_to_" + poi["name"].lower()
        col_name = col_name.replace(" ", "_").replace("(", "").replace(")", "")
        col_name = col_name.replace("&", "and").replace("/", "_")
        col_name = col_name.replace("__", "_").rstrip("_")
        
        df[col_name] = df.apply(
            lambda row, p=poi: round(haversine_miles(row["lat"], row["lon"], p["lat"], p["lon"]), 3)
            if pd.notna(row["lat"]) and pd.notna(row["lon"]) else None,
            axis=1
        )
    
    # find nearest grocery store for each listing
    grocery_pois = [p for p in PLACES_OF_INTEREST if p["category"] == "grocery"]
    grocery_cols = []
    for poi in grocery_pois:
        col = "dist_to_" + poi["name"].lower().replace(" ", "_").replace("(", "").replace(")", "").replace("&", "and").replace("/", "_").replace("__", "_").rstrip("_")
        grocery_cols.append((col, poi["name"]))
    
    def find_nearest(row, cols_and_names):
        """helper to find which POI is closest"""
        best_dist = 999
        best_name = "Unknown"
        for col, name in cols_and_names:
            d = row.get(col)
            if d is not None and d < best_dist:
                best_dist = d
                best_name = name
        return best_name, best_dist
    
    nearest_grocery = df.apply(lambda row: find_nearest(row, grocery_cols), axis=1)
    df["nearest_grocery"] = nearest_grocery.apply(lambda x: x[0])
    df["nearest_grocery_dist"] = nearest_grocery.apply(lambda x: round(x[1], 3))
    
    # find nearest campus building
    campus_pois = [p for p in PLACES_OF_INTEREST if p["category"] == "campus"]
    campus_cols = []
    for poi in campus_pois:
        col = "dist_to_" + poi["name"].lower().replace(" ", "_").replace("(", "").replace(")", "").replace("&", "and").replace("/", "_").replace("__", "_").rstrip("_")
        campus_cols.append((col, poi["name"]))
    
    nearest_campus = df.apply(lambda row: find_nearest(row, campus_cols), axis=1)
    df["nearest_campus"] = nearest_campus.apply(lambda x: x[0])
    df["nearest_campus_dist"] = nearest_campus.apply(lambda x: round(x[1], 3))
    
    # print some stats
    print(f"\n  nearest grocery store distribution:")
    for name, count in df["nearest_grocery"].value_counts().items():
        print(f"    {name}: {count} listings")
    
    print(f"\n  nearest campus building distribution:")
    for name, count in df["nearest_campus"].value_counts().items():
        print(f"    {name}: {count} listings")
    
    avg_campus = df["nearest_campus_dist"].mean()
    avg_grocery = df["nearest_grocery_dist"].mean()
    print(f"\n  avg distance to nearest campus building: {avg_campus:.2f} mi")
    print(f"  avg distance to nearest grocery store: {avg_grocery:.2f} mi")
    
    return df


def get_poi_dataframe():
    """return the POI list as a dataframe
    useful for plotting them on the map alongside listings
    """
    return pd.DataFrame(PLACES_OF_INTEREST)


# ---- run standalone to test ----
if __name__ == "__main__":
    # just print out the POI table to check everything looks right
    poi_df = get_poi_dataframe()
    print("Points of Interest:")
    print(f"{'Name':<35} {'Lat':>10} {'Lon':>12} {'Category':<10}")
    print("-" * 70)
    for _, row in poi_df.iterrows():
        print(f"{row['name']:<35} {row['lat']:>10.4f} {row['lon']:>12.4f} {row['category']:<10}")
    
    # if theres an enriched csv, compute distances on it
    root = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(root, "enriched_listings.csv")
    if os.path.exists(csv_path):
        print(f"\nfound enriched data, computing distances...")
        df = pd.read_csv(csv_path)
        df = compute_all_distances(df)
        
        df.to_csv(csv_path, index=False, encoding="utf-8")
        print(f"\nsaved updated data with distances to {csv_path}")
    else:
        print(f"\nno enriched_listings.csv found - run enrich.py first")
