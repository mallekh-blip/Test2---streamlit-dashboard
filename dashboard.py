import pandas as pd
import streamlit as st
from pymongo import MongoClient
from pymongo.errors import PyMongoError

st.set_page_config(page_title="Movie Catalog Insights", layout="wide")
st.title("Movie Catalog Insights")
st.caption("Data source: Azure DocumentDB")


@st.cache_data(ttl=300)
def load_movies():
    with MongoClient(
        st.secrets["AZURE_URI"],
        username=st.secrets["AZURE_USERNAME"],
        password=st.secrets["AZURE_PASSWORD"],
        serverSelectionTimeoutMS=10000,
    ) as client:
        collection = client["test2_mflix"]["movies_dashboard"]
        fields = {"_id": 0, "title": 1, "year": 1, "genres": 1,
                  "rating": 1, "comment_count": 1}
        return pd.DataFrame(list(collection.find({}, fields)))


try:
    movies = load_movies()
except (PyMongoError, KeyError, FileNotFoundError):
    st.error("Could not read from Azure. Check secrets.toml and the Azure firewall.")
    st.stop()

if movies.empty:
    st.warning("No movie documents were found in Azure.")
    st.stop()

st.success(f"Loaded {len(movies):,} movie documents from Azure.")

genres = sorted({genre for tags in movies["genres"] for genre in tags})
selected = st.sidebar.selectbox("Genre", ["All genres", *genres])
rated_only = st.sidebar.checkbox("Only movies with an IMDb rating")

filtered = movies.copy()
if selected != "All genres":
    filtered = filtered[filtered["genres"].map(lambda tags: selected in tags)]
if rated_only:
    filtered = filtered[filtered["rating"].notna()]

if filtered.empty:
    st.info("No movies match these filters.")
    st.stop()

rated_count = filtered["rating"].notna().sum()
mean_rating = filtered["rating"].mean()
comment_pct = filtered["comment_count"].gt(0).mean() * 100

a, b, c = st.columns(3)
a.metric("Movies", f"{len(filtered):,}")
b.metric("Mean IMDb rating", f"{mean_rating:.2f} / 10" if rated_count else "N/A")
c.metric("Movies with linked comments", f"{comment_pct:.1f}%")
st.caption(f"The mean rating uses {rated_count:,} rated movies.")

dated = filtered.dropna(subset=["year"]).assign(
    decade=lambda df: (df["year"].astype(int) // 10) * 10
)
if not dated.empty:
    by_decade = dated.groupby("decade")["rating"].agg(
        movie_count="size", rated_count="count", mean_rating="mean"
    )
    st.subheader("Movie count by release decade")
    st.bar_chart(by_decade["movie_count"])
    st.subheader("Mean IMDb rating by release decade")
    st.line_chart(by_decade["mean_rating"])
    st.dataframe(by_decade.round(2))

st.subheader("Movies with the most linked comments")
st.dataframe(
    filtered.nlargest(10, "comment_count")[
        ["title", "year", "rating", "comment_count"]
    ],
    hide_index=True,
)
st.caption("Linked comments describe recorded activity in this sample, not viewership or sentiment.")