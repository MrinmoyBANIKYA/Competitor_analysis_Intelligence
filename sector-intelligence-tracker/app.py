"""
app.py
------
Main Streamlit dashboard for the Sector Intelligence Tracker.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from data.scrapers import (
    get_playstore_ratings,
    get_google_trends,
    get_news_mentions,
    get_linkedin_job_count,
    get_ambitionbox_rating,
)
from data.sectors import SECTORS, list_sector_keys
from utils.helpers import format_large_number, timestamp_label

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Sector Intelligence Tracker",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", "")
CHART_COLORS = ["#378ADD", "#1D9E75", "#D85A30", "#7F77DD", "#BA7517", "#D4537E"]

# ---------------------------------------------------------------------------
# Custom CSS — match the Stitch design reference
# ---------------------------------------------------------------------------

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

.stApp {
    background-color: #F7F9FB !important;
    color: #191C1E;
}
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; }

/* Title */
.dashboard-title {
    font-family: 'Manrope', sans-serif;
    font-weight: 800; font-size: 1.55rem;
    color: #0D3B66; letter-spacing: -0.03em;
    margin: 0; padding: 0.2rem 0;
}
.dashboard-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem; color: #717783;
    font-weight: 500; margin-top: -2px;
}

/* Metric cards */
[data-testid="stMetricValue"] {
    font-family: 'Manrope', sans-serif !important;
    font-weight: 800 !important; font-size: 2rem !important;
    color: #191C1E !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important; font-size: 0.7rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important; color: #414751 !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important; font-size: 0.78rem !important;
}

/* Card wrappers */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border-radius: 12px !important;
    border: 1px solid rgba(192,199,211,0.15) !important;
    box-shadow: 0px 12px 32px rgba(25,28,30,0.04);
}

/* Chart titles */
.chart-title {
    font-family: 'Manrope', sans-serif;
    font-weight: 700; font-size: 1.05rem;
    color: #191C1E; margin-bottom: 0.15rem;
}
.chart-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem; color: #717783; font-weight: 500;
}

/* Insight box */
.insight-box {
    border-left: 4px solid #378ADD;
    background: rgba(55,138,221,0.06);
    padding: 1.2rem 1.5rem; border-radius: 0 12px 12px 0;
    margin: 1rem 0 2rem 0;
}
.insight-box h4 {
    font-family: 'Manrope', sans-serif;
    font-weight: 700; color: #378ADD;
    margin: 0 0 0.35rem 0; font-size: 0.95rem;
}
.insight-box p {
    font-family: 'Inter', sans-serif;
    color: #414751; font-weight: 500;
    line-height: 1.7; margin: 0; font-size: 0.87rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #F0F2F4 !important;
    border-right: 1px solid #E0E3E5;
}
.sidebar-footer {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem; color: #717783;
    text-align: center; padding: 1rem;
    border-top: 1px solid #E0E3E5; margin-top: 2rem;
}
.sidebar-footer strong { color: #378ADD; }

/* Selectbox */
[data-testid="stSelectbox"] label {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important; font-size: 0.75rem !important;
    text-transform: uppercase; letter-spacing: 0.05em; color: #414751 !important;
}

/* Buttons */
.stButton > button, .stDownloadButton > button {
    background-color: #378ADD !important; color: white !important;
    font-family: 'Manrope', sans-serif !important;
    font-weight: 700 !important; font-size: 0.82rem !important;
    border-radius: 8px !important; border: none !important;
    padding: 0.55rem 1.4rem !important;
    box-shadow: 0 2px 8px rgba(55,138,221,0.25) !important;
    transition: all 0.15s ease-in-out !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background-color: #2A74C4 !important;
    box-shadow: 0 4px 16px rgba(55,138,221,0.35) !important;
}
.stButton > button:active { transform: scale(0.97); }
.stSpinner > div { color: #378ADD !important; }

.section-divider {
    border: none; border-top: 1px solid #E0E3E5; margin: 2rem 0;
}
</style>""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Cached data loaders
# ---------------------------------------------------------------------------

@st.cache_data(ttl=3600, show_spinner=False)
def cached_playstore_ratings(sector_key: str) -> dict:
    return get_playstore_ratings(SECTORS[sector_key].get("app_ids", {}))

@st.cache_data(ttl=3600, show_spinner=False)
def cached_google_trends(sector_key: str) -> pd.DataFrame:
    companies = SECTORS[sector_key]["companies"]
    return get_google_trends(companies[:5], timeframe="today 12-m")

@st.cache_data(ttl=3600, show_spinner=False)
def cached_news_mentions(sector_key: str, api_key: str) -> dict:
    if not api_key:
        return {c: 0 for c in SECTORS[sector_key]["companies"]}
    return get_news_mentions(SECTORS[sector_key]["companies"], api_key)

@st.cache_data(ttl=3600, show_spinner=False)
def cached_linkedin_jobs(sector_key: str) -> dict:
    return get_linkedin_job_count(SECTORS[sector_key].get("linkedin_slugs", {}))

@st.cache_data(ttl=3600, show_spinner=False)
def cached_ambitionbox(sector_key: str) -> dict:
    return get_ambitionbox_rating(SECTORS[sector_key]["companies"])

# ---------------------------------------------------------------------------
# Chart helpers
# ---------------------------------------------------------------------------

def apply_layout(fig, height=400):
    """Apply the editorial chart theme matching the Stitch design."""
    fig.update_layout(
        title=None,
        font=dict(family="Inter, sans-serif", size=12, color="#414751"),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=20, t=20, b=40), height=height,
        xaxis=dict(showgrid=False, tickfont=dict(family="Inter", size=10, color="#717783"), linecolor="#E0E3E5"),
        yaxis=dict(showgrid=True, gridcolor="#F0F2F4", gridwidth=1, tickfont=dict(family="Inter", size=10, color="#717783"), linecolor="#E0E3E5"),
        legend=dict(font=dict(family="Inter", size=11, color="#414751"), bgcolor="rgba(0,0,0,0)", borderwidth=0, orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter", bordercolor="#E0E3E5"),
    )
    return fig

def color_map_for(companies):
    return {c: CHART_COLORS[i % len(CHART_COLORS)] for i, c in enumerate(companies)}

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:1.5rem 0 1rem 0;'>
        <div style='width:56px;height:56px;border-radius:50%;
             background:linear-gradient(135deg,#378ADD 0%,#1D6BBF 100%);
             margin:0 auto 0.8rem auto;display:flex;align-items:center;justify-content:center;'>
            <span style='font-size:1.5rem;'>📡</span>
        </div>
        <p style='font-family:Manrope,sans-serif;font-weight:800;font-size:1rem;color:#191C1E;margin:0;'>Sector Intel</p>
        <p style='font-family:Inter,sans-serif;font-size:0.75rem;color:#717783;margin:0.2rem 0 0 0;'>Bangalore Startup Tracker</p>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"🕐 Last refresh: **{timestamp_label()}**")
    st.markdown("---")
    st.sidebar.markdown("Built by Mrinmoy Banikya · Bangalore 2026")

# ---------------------------------------------------------------------------
# Top bar
# ---------------------------------------------------------------------------

top1, top2, top3 = st.columns([3, 2, 1])

with top1:
    st.markdown("""
    <p class='dashboard-title'>Sector Intelligence Tracker</p>
    <p class='dashboard-subtitle'>Live competitive intelligence across India's startup ecosystem</p>
    """, unsafe_allow_html=True)

with top2:
    selected_sector = st.selectbox("SELECT SECTOR", list_sector_keys(), index=0, key="sector_selector")

with top3:
    st.markdown("<br>", unsafe_allow_html=True)
    generate_pdf = st.button("📄 Generate PDF", use_container_width=True)

# ---------------------------------------------------------------------------
# Load sector data
# ---------------------------------------------------------------------------

sector_config = SECTORS[selected_sector]
companies = sector_config["companies"]
cmap = color_map_for(companies)

with st.spinner("Fetching live data..."):
    ratings_data = cached_playstore_ratings(selected_sector)
    trends_df    = cached_google_trends(selected_sector)
    news_data    = cached_news_mentions(selected_sector, NEWS_API_KEY)
    jobs_data    = cached_linkedin_jobs(selected_sector)
    employer_data = cached_ambitionbox(selected_sector)

# ---------------------------------------------------------------------------
# Compute headline metrics
# ---------------------------------------------------------------------------

# Avg app rating
if ratings_data:
    rv = [v["rating"] for v in ratings_data.values() if v["rating"] > 0]
    avg_rating = round(sum(rv) / len(rv), 1) if rv else 0.0
else:
    avg_rating = 0.0

# Top hiring company
if jobs_data:
    top_hire_co = max(jobs_data, key=jobs_data.get)
    top_hire_n  = jobs_data[top_hire_co]
else:
    top_hire_co, top_hire_n = "N/A", 0

# Brand leader from trends
brand_leader, brand_share = "N/A", 0
if not trends_df.empty:
    tcols = [c for c in trends_df.columns if c not in ("date", "isPartial")]
    if tcols:
        avgs = trends_df[tcols].mean()
        brand_leader = avgs.idxmax()
        total = avgs.sum()
        brand_share = int(round((avgs[brand_leader] / total) * 100)) if total > 0 else 0

# Total news
total_news = sum(news_data.values()) if news_data else 0

# ---------------------------------------------------------------------------
# Metric row
# ---------------------------------------------------------------------------

st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)

with m1:
    with st.container(border=True):
        st.metric("Avg App Rating", f"{avg_rating}" if avg_rating else "N/A", delta="Play Store" if avg_rating else None)
with m2:
    with st.container(border=True):
        st.metric("Top Hiring Co", top_hire_co, delta=f"{top_hire_n} open roles")
with m3:
    with st.container(border=True):
        st.metric("Brand Leader", brand_leader, delta=f"Share of Voice: {brand_share}%")
with m4:
    with st.container(border=True):
        st.metric("News Mentions (30d)", format_large_number(total_news) if total_news else "N/A", delta="All companies" if total_news else None)

# ---------------------------------------------------------------------------
# Insight box
# ---------------------------------------------------------------------------

st.markdown(f"""
<div class='insight-box'>
    <h4>💡 Sector Momentum Insight</h4>
    <p>{sector_config["insight"]}</p>
</div>""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Charts Row 1 — App Ratings + Hiring Velocity
# ---------------------------------------------------------------------------

c1, c2 = st.columns(2)

with c1:
    with st.container(border=True):
        st.markdown("<p class='chart-title'>App Store Ratings</p><p class='chart-subtitle'>Google Play Store · Scale 0–5</p>", unsafe_allow_html=True)
        if ratings_data:
            rdf = pd.DataFrame([{"Company": k, "Rating": v["rating"], "Reviews": v["num_ratings"]} for k, v in ratings_data.items() if v["rating"] > 0])
            if not rdf.empty:
                fig1 = px.bar(rdf, x="Company", y="Rating", color="Company", color_discrete_map=cmap, text="Rating")
                fig1.update_traces(textposition="outside", textfont=dict(family="Manrope", size=13, color="#191C1E"), marker_line_width=0, marker_cornerradius=6)
                fig1.update_yaxes(range=[0, 5.5])
                apply_layout(fig1, 380)
                fig1.update_layout(showlegend=False)
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("No app rating data available for this sector.")
        else:
            st.info("No Play Store apps configured for this sector.")

with c2:
    with st.container(border=True):
        st.markdown("<p class='chart-title'>Hiring Velocity</p><p class='chart-subtitle'>Open LinkedIn roles per company</p>", unsafe_allow_html=True)
        if jobs_data and any(v > 0 for v in jobs_data.values()):
            jdf = pd.DataFrame([{"Company": k, "Open Roles": v} for k, v in jobs_data.items()]).sort_values("Open Roles", ascending=False)
            fig2 = px.bar(jdf, x="Company", y="Open Roles", color="Company", color_discrete_map=cmap, text="Open Roles")
            fig2.update_traces(textposition="outside", textfont=dict(family="Manrope", size=13, color="#191C1E"), marker_line_width=0, marker_cornerradius=6)
            apply_layout(fig2, 380)
            fig2.update_layout(showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("LinkedIn job data unavailable — may require retry.")

# ---------------------------------------------------------------------------
# Chart 3 — Google Trends (full width)
# ---------------------------------------------------------------------------

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("<p class='chart-title'>Brand Momentum — Google Trends (12 Months)</p><p class='chart-subtitle'>Search interest over time · India</p>", unsafe_allow_html=True)
    if not trends_df.empty:
        tdf = trends_df.drop(columns=["isPartial"], errors="ignore")
        if tdf.index.name == "date" or "date" not in tdf.columns:
            tdf = tdf.reset_index()
        date_col = tdf.columns[0]
        val_cols = [c for c in tdf.columns if c != date_col]
        long = tdf.melt(id_vars=[date_col], value_vars=val_cols, var_name="Company", value_name="Interest")
        fig3 = px.line(long, x=date_col, y="Interest", color="Company", color_discrete_map=cmap)
        fig3.update_traces(line=dict(width=2.5))
        apply_layout(fig3, 420)
        fig3.update_layout(xaxis_title=None, yaxis_title="Search Interest (0–100)")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Google Trends data is currently unavailable.")

# ---------------------------------------------------------------------------
# Charts Row 3 — Scatter + News Mentions
# ---------------------------------------------------------------------------

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
c3, c4 = st.columns(2)

with c3:
    with st.container(border=True):
        st.markdown("<p class='chart-title'>News Mentions vs Employer Score</p><p class='chart-subtitle'>Bubble position = competitive positioning</p>", unsafe_allow_html=True)
        sdf = pd.DataFrame([{"Company": co, "News Mentions": news_data.get(co, 0), "Employer Score": employer_data.get(co, 3.5)} for co in companies])
        fig4 = px.scatter(sdf, x="News Mentions", y="Employer Score", color="Company", color_discrete_map=cmap, text="Company")
        fig4.update_traces(marker=dict(size=20, line=dict(width=1.5, color="white")), textposition="top center", textfont=dict(family="Inter", size=10, color="#414751"))
        apply_layout(fig4, 400)
        fig4.update_layout(showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

with c4:
    with st.container(border=True):
        st.markdown("<p class='chart-title'>News Mention Frequency</p><p class='chart-subtitle'>Article count · Past 30 days</p>", unsafe_allow_html=True)
        if news_data and any(v > 0 for v in news_data.values()):
            ndf = pd.DataFrame([{"Company": k, "Mentions": v} for k, v in news_data.items()]).sort_values("Mentions", ascending=True)
            fig5 = px.bar(ndf, x="Mentions", y="Company", color="Company", color_discrete_map=cmap, orientation="h", text="Mentions")
            fig5.update_traces(textposition="outside", textfont=dict(family="Manrope", size=12, color="#191C1E"), marker_line_width=0, marker_cornerradius=6)
            apply_layout(fig5, 400)
            fig5.update_layout(showlegend=False, yaxis_title=None)
            st.plotly_chart(fig5, use_container_width=True)
        else:
            st.info("News data unavailable — check NEWS_API_KEY in .streamlit/secrets.toml")

# ---------------------------------------------------------------------------
# PDF Generation
# ---------------------------------------------------------------------------

if generate_pdf:
    try:
        from reports.pdf_generator import generate_report
        pdf_bytes = generate_report(
            sector_name=selected_sector,
            company_name=companies[0] if companies else selected_sector,
            df_ratings=ratings_data,
            df_hiring=jobs_data,
            df_news=news_data,
            df_glassdoor=employer_data,
            insight_text=sector_config["insight"],
            personalised_line_1=f"{companies[0]} shows distinctive positioning in the {selected_sector} landscape." if companies else "",
            personalised_line_2=sector_config["insight"],
        )
        if pdf_bytes:
            st.download_button(
                "⬇ Download PDF Report",
                data=pdf_bytes,
                file_name=f"{selected_sector.lower().replace(' ', '_')}_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.warning("PDF generation returned empty output.")
    except Exception as e:
        st.error(f"PDF generation failed: {e}")
        st.info("Ensure fpdf2 and kaleido are installed.")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

st.markdown("""
<div style='text-align:center;padding:3rem 0 1rem 0;color:#C0C7D3;font-family:Inter,sans-serif;font-size:0.72rem;'>
    Sector Intelligence Tracker · Built with Streamlit + Plotly · Data from public APIs<br>
    © 2026 Mrinmoy Banikya · Bangalore
</div>""", unsafe_allow_html=True)
