# Gunrock-s-Grid

Aggie housing analysis. Short project which demonstrates all ETL cycle and has analytics

we have commented the libraries we used because there was
error when hosting on streamlit
please uncomment the libraries to run the SCRAPER on your local machine

STEPS TO BUILD ENTIRE PROJECT -

1. Uncomment the libraries with their versions and download requirements.txt
2. Run the scraper file - `craiglist_scraper.py`
3. We later manually had added the oncampus housing and its stored in `on_campus_listings.py` so run this file
4. Run the python file which will add more cols in the csv - `enrich.py`
5. The visualization and charts are present in `analysis.ipynb`
6. Run Streamlit to see the project

If you want to run streamlit only then follow -

STEPS TO RUN STREAMLIT ON PC -

1. Download the requirements libraries
2. run this command in terminal - `streamlit run app.py`
