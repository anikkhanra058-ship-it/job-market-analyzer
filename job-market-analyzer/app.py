
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Job Market Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# 2. CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #f3f6f5;
}

header {
    background-color: transparent;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

section[data-testid="stSidebar"] {
    background-color: #e4eeeb;
}

section[data-testid="stSidebar"] h2 {
    color: #244b43;
}

.dashboard-header {
    background: #35564e;
    padding: 28px 32px;
    border-radius: 18px;
    color: white;
    margin-bottom: 22px;
}

.dashboard-header h1 {
    color: white;
    font-size: 29px;
    margin: 0;
}

.dashboard-header p {
    color: #d9e7e2;
    margin-top: 8px;
    font-size: 14px;
}

.metric-card {
    background: white;
    padding: 20px 16px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 2px 9px rgba(0,0,0,0.05);
    min-height: 112px;
}

.metric-label {
    color: #65736e;
    font-size: 13px;
    font-weight: 600;
}

.metric-value {
    color: #263f38;
    font-size: 27px;
    font-weight: 700;
    margin-top: 10px;
}

.section-title {
    color: #294c43;
    font-size: 20px;
    font-weight: 700;
    margin-top: 12px;
    margin-bottom: 12px;
}

.chart-container {
    background: white;
    border-radius: 15px;
    padding: 12px;
    border: 1px solid #e7ece9;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. LOAD DATA
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "cleaned_job_postings.csv"

@st.cache_data
def load_data():

    data = pd.read_csv(DATA_PATH)

    data["salary_min_usd"] = pd.to_numeric(
        data["salary_min_usd"], errors="coerce"
    )

    data["salary_max_usd"] = pd.to_numeric(
        data["salary_max_usd"], errors="coerce"
    )

    data["salary_midpoint"] = (
        data["salary_min_usd"] +
        data["salary_max_usd"]
    ) / 2

    return data


try:
    df = load_data()

except FileNotFoundError:
    st.error("Dataset not found. Check your data folder.")
    st.stop()


# ==========================================
# 4. SIDEBAR FILTERS
# ==========================================

st.sidebar.markdown("## 🔎 Dashboard Filters")

countries = sorted(df["country"].dropna().unique())

selected_countries = st.sidebar.multiselect(
    "Country",
    countries,
    default=countries
)

seniorities = sorted(df["seniority"].dropna().unique())

selected_seniority = st.sidebar.multiselect(
    "Experience Level",
    seniorities,
    default=seniorities
)

remote_options = sorted(df["remote"].dropna().unique())

selected_remote = st.sidebar.multiselect(
    "Work Type",
    remote_options,
    default=remote_options
)

cities = sorted(df["city"].dropna().unique())

selected_cities = st.sidebar.multiselect(
    "City",
    cities
)

# Apply filters

filtered_df = df.copy()

if selected_countries:
    filtered_df = filtered_df[
        filtered_df["country"].isin(selected_countries)
    ]

if selected_seniority:
    filtered_df = filtered_df[
        filtered_df["seniority"].isin(selected_seniority)
    ]

if selected_remote:
    filtered_df = filtered_df[
        filtered_df["remote"].isin(selected_remote)
    ]

if selected_cities:
    filtered_df = filtered_df[
        filtered_df["city"].isin(selected_cities)
    ]


# ==========================================
# 5. HEADER
# ==========================================

st.markdown("""
<div class="dashboard-header">

<h1>📊 JOB MARKET DISTRIBUTION DASHBOARD</h1>

<p>
Explore employment trends, salary distributions,
in-demand skills and job opportunities worldwide.
</p>

</div>
""", unsafe_allow_html=True)


# ==========================================
# 6. KPI CARDS
# ==========================================

total_jobs = len(filtered_df)

avg_salary = filtered_df["salary_midpoint"].mean()

total_countries = filtered_df["country"].nunique()

total_titles = filtered_df["title"].nunique()

def metric_card(label, value):

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card("TOTAL JOB POSTINGS", f"{total_jobs:,}")

with c2:
    salary_text = f"${avg_salary:,.0f}" if pd.notna(avg_salary) else "N/A"
    metric_card("AVERAGE SALARY", salary_text)

with c3:
    metric_card("COUNTRIES", str(total_countries))

with c4:
    metric_card("JOB TITLES", str(total_titles))


st.markdown("<br>", unsafe_allow_html=True)


# ==========================================
# 7. JOB TITLE DISTRIBUTION
# ==========================================

st.markdown(
    '<div class="section-title">💼 Job Role Distribution</div>',
    unsafe_allow_html=True
)

role_counts = filtered_df["title"].value_counts().head(6)

c1, c2 = st.columns(2)

with c1:

    if not role_counts.empty:

        fig = px.pie(
            names=role_counts.index,
            values=role_counts.values,
            hole=0.62,
            color_discrete_sequence=px.colors.sequential.Teal
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent"
        )

        fig.update_layout(
            title="Top Job Titles",
            showlegend=True,
            height=340,
            margin=dict(t=45, b=10, l=10, r=10),
            paper_bgcolor="white"
        )

        st.plotly_chart(fig, use_container_width=True)

with c2:

    seniority_counts = filtered_df["seniority"].value_counts()

    fig = px.pie(
        names=seniority_counts.index,
        values=seniority_counts.values,
        hole=0.62,
        color_discrete_sequence=px.colors.sequential.Greens
    )

    fig.update_layout(
        title="Experience Level Distribution",
        height=340,
        margin=dict(t=45, b=10, l=10, r=10),
        paper_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)


# ==========================================
# 8. WORK TYPE DISTRIBUTION
# ==========================================

st.markdown(
    '<div class="section-title">🏢 Work Type Distribution</div>',
    unsafe_allow_html=True
)

c1, c2 = st.columns(2)

with c1:

    remote_counts = filtered_df["remote"].value_counts()

    fig = px.pie(
        names=remote_counts.index,
        values=remote_counts.values,
        hole=0.6,
        color_discrete_sequence=px.colors.sequential.Teal
    )

    fig.update_layout(
        title="Remote / Onsite / Hybrid",
        height=330,
        paper_bgcolor="white",
        margin=dict(t=45, b=10, l=10, r=10)
    )

    st.plotly_chart(fig, use_container_width=True)

with c2:

    city_counts = filtered_df["city"].value_counts().head(8)

    fig = px.bar(
        x=city_counts.values,
        y=city_counts.index,
        orientation="h",
        title="Top Hiring Cities",
        labels={
            "x": "Job Listings",
            "y": "City"
        },
        color=city_counts.values,
        color_continuous_scale="Teal"
    )

    fig.update_layout(
        height=330,
        showlegend=False,
        coloraxis_showscale=False,
        paper_bgcolor="white",
        margin=dict(t=45, b=10, l=10, r=10)
    )

    st.plotly_chart(fig, use_container_width=True)


# ==========================================
# 9. COUNTRY DISTRIBUTION MAP
# ==========================================

st.markdown(
    '<div class="section-title">🌍 Global Job Distribution</div>',
    unsafe_allow_html=True
)

# Convert ISO-2 country codes into ISO-3 codes

country_mapping = {
    "BR": "BRA",
    "CA": "CAN",
    "DE": "DEU",
    "GB": "GBR",
    "IN": "IND",
    "NL": "NLD",
    "US": "USA"
}

map_data = (
    filtered_df["country"]
    .value_counts()
    .rename_axis("country")
    .reset_index(name="job_count")
)

map_data["iso3"] = map_data["country"].map(country_mapping)

map_data = map_data.dropna(subset=["iso3"])

if not map_data.empty:

    fig = px.choropleth(
        map_data,
        locations="iso3",
        color="job_count",
        hover_name="country",
        color_continuous_scale="Teal",
        title="Job Listings by Country",
        labels={"job_count": "Job Listings"}
    )

    fig.update_layout(
        height=420,
        paper_bgcolor="white",
        margin=dict(t=45, b=10, l=10, r=10)
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("No mapped country data available.")


# ==========================================
# 10. TOP IN-DEMAND SKILLS
# ==========================================

st.markdown(
    '<div class="section-title">🔥 Top In-Demand Skills</div>',
    unsafe_allow_html=True
)

all_skills = (
    filtered_df["skills"]
    .dropna()
    .str.split("|")
    .explode()
    .str.strip()
    .str.lower()
)

top_skills = all_skills.value_counts().head(10)

if not top_skills.empty:

    fig = px.bar(
        x=top_skills.values,
        y=top_skills.index,
        orientation="h",
        labels={
            "x": "Number of Job Listings",
            "y": "Skill"
        },
        color=top_skills.values,
        color_continuous_scale="Teal",
        title="Top 10 Most In-Demand Skills"
    )

    fig.update_layout(
        height=420,
        yaxis={"categoryorder": "total ascending"},
        coloraxis_showscale=False,
        paper_bgcolor="white",
        margin=dict(t=45, b=10, l=10, r=10)
    )

    st.plotly_chart(fig, use_container_width=True)


# ==========================================
# 11. SALARY ANALYSIS
# ==========================================

st.markdown(
    '<div class="section-title">💰 Salary Analysis</div>',
    unsafe_allow_html=True
)

salary_data = filtered_df.dropna(
    subset=["salary_midpoint"]
)

if not salary_data.empty:

    c1, c2 = st.columns(2)

    with c1:

        fig = px.histogram(
            salary_data,
            x="salary_midpoint",
            nbins=20,
            title="Salary Distribution",
            labels={
                "salary_midpoint": "Salary (USD)"
            },
            color_discrete_sequence=["#397b6b"]
        )

        fig.update_layout(
            height=350,
            paper_bgcolor="white"
        )

        st.plotly_chart(fig, use_container_width=True)

    with c2:

        salary_by_title = (
            salary_data.groupby("title")
            .agg(
                average_salary=("salary_midpoint", "mean"),
                listings=("salary_midpoint", "count")
            )
            .query("listings >= 10")
            .sort_values("average_salary", ascending=False)
            .head(10)
            .reset_index()
        )

        if not salary_by_title.empty:

            fig = px.bar(
                salary_by_title,
                x="average_salary",
                y="title",
                orientation="h",
                title="Highest Paying Job Titles",
                color="average_salary",
                color_continuous_scale="Teal",
                labels={
                    "average_salary": "Average Salary (USD)",
                    "title": "Job Title"
                }
            )

            fig.update_layout(
                height=350,
                yaxis={"categoryorder": "total ascending"},
                coloraxis_showscale=False,
                paper_bgcolor="white"
            )

            st.plotly_chart(fig, use_container_width=True)

else:
    st.info("No salary data available for the selected filters.")


# ==========================================
# 12. JOB LISTINGS TABLE
# ==========================================

st.markdown(
    '<div class="section-title">📋 Explore Job Listings</div>',
    unsafe_allow_html=True
)

search = st.text_input("Search jobs, cities or skills")

display_df = filtered_df.copy()

if search:

    mask = (
        display_df["title"].fillna("").str.contains(
            search, case=False
        )
        |
        display_df["city"].fillna("").str.contains(
            search, case=False
        )
        |
        display_df["skills"].fillna("").str.contains(
            search, case=False
        )
    )

    display_df = display_df[mask]

st.dataframe(
    display_df.drop(columns=["salary_midpoint"]),
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "⬇ Download Job Listings",
    data=display_df.to_csv(index=False).encode("utf-8"),
    file_name="job_market_data.csv",
    mime="text/csv"
)


# ==========================================
# 13. FOOTER
# ==========================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#718078;">
        Job Market Analyzer | Built with Python, Pandas,
        Plotly and Streamlit
        <br>
        <small>
        Dataset is synthetic and intended for demonstration purposes.
        </small>
    </div>
    """,
    unsafe_allow_html=True
)
