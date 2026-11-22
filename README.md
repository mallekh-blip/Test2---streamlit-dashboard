# Movie Catalog Insights

**Author:** Mallekedi Hari Babu

[Open the live Streamlit dashboard](https://test2---app-dashboard-6vtuckwuzsuaw72d7appmcd.streamlit.app)

I built this dashboard to help a streaming service’s catalog team explore its movie
collection and identify genres or release decades that may be underrepresented.
The dashboard reads 21,117 movie documents from Azure DocumentDB.

## What the dashboard shows

- Movie count, average IMDb rating, and the percentage of movies with linked comments
- Movie counts and average IMDb ratings by release decade
- Movies with the most linked comments
- Filters for genre and whether a movie has an IMDb rating

For example, filtering to Horror shows 1,461 movies. Of those, 1,456 have
an IMDb rating, averaging 5.78 out of 10. The release-decade chart can help
a catalog manager decide which periods to research for a classic horror
collection. I would check subscriber search and viewing data before making a
licensing decision, because catalog counts and linked comments do not measure demand.

## Database connection

- **Platform:** Azure DocumentDB (MongoDB compatible)
- **Database:** `test2_mflix`
- **Collection:** `movies_dashboard`
- **Structure:** One document per movie, with the fields needed by the dashboard,
  including release year, genres, IMDb rating, and linked comment count.

The app connects to Azure using PyMongo and reads its connection settings
from Streamlit Secrets. You do not need database credentials to view the
live dashboard. Running it locally requires authorized database access.

## Run locally

1. Clone this repository and open it in VS Code.
2. Install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Create `.streamlit/secrets.toml` in the project folder and enter your
   authorized Azure connection details. The values below are placeholders:

   ```toml
   AZURE_URI = "YOUR_AZURE_MONGODB_CONNECTION_URI"
   AZURE_USERNAME = "YOUR_DATABASE_USERNAME"
   AZURE_PASSWORD = "YOUR_DATABASE_PASSWORD"
   ```

4. Start the dashboard:

   ```powershell
   python -m streamlit run dashboard.py
   ```
