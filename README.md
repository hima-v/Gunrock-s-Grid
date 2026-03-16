# Gunrock's Grid

Aggie housing analysis. Short project which demonstrates the full ETL cycle with some analytics.

> The libraries in `requirements.txt` are commented out due to a Streamlit hosting error.
> Uncomment them before running the scraper on your local machine.

---

## Steps to Build the Entire Project

1. Uncomment the libraries with their versions and download `requirements.txt`
2. Run the scraper file — `craiglist_scraper.py`
3. We manually added the on-campus housing data, stored in `on_campus_listings.py` — run this next
4. Run the enrichment file which adds more columns to the CSV — `enrich.py`
5. Visualizations and charts are in `analysis.ipynb`
6. Run Streamlit to see the project

---

## Steps to Run Streamlit Only

1. Download the required libraries
2. Run this command in terminal:

```bash
   streamlit run app.py
```

---

## Note

One listing on Craigslist is incorrect — it's dividing the price by number of rooms, but it's actually the price per room. This is a limitation of the data since what we get depends on what the owner posts on Craigslist. We could have fixed that listing but kept it in to demonstrate this limitation.
