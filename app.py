import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- Page Config ----------------

st.set_page_config(
    page_title="Netflix AI Dashboard",
    layout="wide"
)

st.title("🎬 Netflix AI Dashboard")

# ---------------- Load Dataset ----------------

df = pd.read_csv("netflix.csv")

# ---------------- Data Cleaning ----------------

df = df.drop_duplicates()
df.fillna("Unknown", inplace=True)

st.header("🧹 Data Cleaning")

missing_values = df.isnull().sum()

st.write("Missing Values in Dataset")
st.dataframe(missing_values)

# ---------------- Sidebar Filters ----------------

st.sidebar.header("Filters")

selected_type = st.sidebar.selectbox(
    "Select Type",
    ["All"] + list(df["type"].unique())
)

if selected_type != "All":
    df = df[df["type"] == selected_type]

# ---------------- Dataset Preview ----------------

st.subheader("Dataset Preview")

st.dataframe(df.head())

st.write("Rows:", df.shape[0])
st.write("Columns:", df.shape[1])

# ---------------- KPI Cards ----------------

st.header("📊 Key Metrics")

total_titles = len(df)
movies = len(df[df["type"] == "Movie"])
tv_shows = len(df[df["type"] == "TV Show"])
countries = df["country"].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Titles", total_titles)
c2.metric("Movies", movies)
c3.metric("TV Shows", tv_shows)
c4.metric("Countries", countries)

# ---------------- Visualizations ----------------

st.header("📈 Visualizations")

# Row 1

col1, col2 = st.columns(2)

with col1:
    type_count = df["type"].value_counts()

    fig1 = px.pie(
        names=type_count.index,
        values=type_count.values,
        title="Movies vs TV Shows"
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:
    country_count = (
        df[df["country"] != "Unknown"]["country"]
        .value_counts()
        .head(10)
    )

    fig2 = px.bar(
        x=country_count.index,
        y=country_count.values,
        title="Top 10 Countries"
    )

    st.plotly_chart(fig2, use_container_width=True)

# Row 2

col3, col4 = st.columns(2)

with col3:
    rating_count = df["rating"].value_counts()

    fig3 = px.bar(
        x=rating_count.index,
        y=rating_count.values,
        title="Ratings Distribution"
    )

    st.plotly_chart(fig3, use_container_width=True)

with col4:
    df["date_added"] = pd.to_datetime(
        df["date_added"],
        errors="coerce"
    )

    df["year_added"] = df["date_added"].dt.year

    year_count = df["year_added"].value_counts().sort_index()

    fig4 = px.line(
        x=year_count.index,
        y=year_count.values,
        title="Content Added Over Years"
    )

    st.plotly_chart(fig4, use_container_width=True)

# Row 3

genre_count = df["listed_in"].value_counts().head(10)

fig5 = px.bar(
    x=genre_count.index,
    y=genre_count.values,
    title="Top Genres"
)

st.plotly_chart(fig5, use_container_width=True)

# ---------------- Download Button ----------------

st.header("📥 Download Filtered Data")

csv = df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_netflix_data.csv",
    mime="text/csv"
)