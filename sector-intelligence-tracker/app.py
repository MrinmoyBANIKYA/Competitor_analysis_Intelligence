"""
app.py
------
Main Streamlit dashboard for the Sector Intelligence Tracker.
Redesigned with NixTio modern dark theme layout, CSS animations, and simple Auth.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

from data.scrapers import (
    get_playstore_ratings,
    get_google_trends,
    get_news_mentions,
    get_linkedin_job_count,
    get_ambitionbox_rating,
    get_review_sentiment,
)
from data.sectors import SECTORS, list_sector_keys
from data.sector_meta import SECTOR_META
from utils.helpers import format_large_number, timestamp_label

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Sector Intelligence Tracker",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize Session State Variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", "")
CHART_COLORS = ["#B388FF", "#D4E157", "#9E9E9E", "#FFB74D", "#81C784", "#CE93D8"]

# ---------------------------------------------------------------------------
# Advanced Custom CSS — Premium Authentic Animations
# ---------------------------------------------------------------------------

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

/* Dynamic Animated Background */
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Base App Wrapper with Moving Gradient Background */
.stApp {
    background: linear-gradient(-45deg, #0B0B0C, #120D23, #091218, #0B0B0C);
    background-size: 400% 400%;
    animation: gradientBG 18s ease infinite;
    color: #FFFFFF;
}

/* Hide Streamlit Standard Elements */
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; display: none; }

/* Apply Fade-in to main app views */
[data-testid="stVerticalBlock"] {
    animation: fadeIn 0.8s ease-out forwards;
}

/* -----------------------------------------------------
 * Login Page Specific
 * ----------------------------------------------------- */
.login-box {
    background-color: #15111B;
    border: 1px solid #2A1A4A;
    border-radius: 20px;
    padding: 3rem;
    box-shadow: 0 15px 40px rgba(0,0,0,0.5);
    text-align: center;
    max-width: 450px;
    margin: auto;
    margin-top: 10vh;
    animation: fadeIn 1s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.login-title {
    font-family: 'Manrope', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 0.5rem;
}
.login-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    color: #8E8D92;
    margin-bottom: 2.5rem;
}

/* -----------------------------------------------------
 * Dashboard Main Styling
 * ----------------------------------------------------- */

/* Dashboard Titles */
.dashboard-title {
    font-family: 'Manrope', sans-serif;
    font-weight: 800; font-size: 1.8rem;
    color: #FFFFFF; letter-spacing: -0.02em;
    margin: 0; padding: 0;
}
.dashboard-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem; color: #8E8D92;
    font-weight: 500; margin-top: 2px;
}

/* Metric Cards */
[data-testid="stMetricValue"] {
    font-family: 'Manrope', sans-serif !important;
    font-weight: 700 !important; font-size: 1.8rem !important;
    color: #FFFFFF !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important; font-size: 0.75rem !important;
    color: #8E8D92 !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important; font-size: 0.75rem !important;
    color: #B388FF !important;
}

/* Modern Card Wrappers with Hover Animations */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #15111B !important;
    border-radius: 20px !important;
    border: 1px solid #2A1A4A !important;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
    padding: 0.5rem;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-5px);
    box-shadow: 0px 12px 25px rgba(179, 136, 255, 0.1);
    border-color: #B388FF !important;
}

/* Chart Titles */
.chart-title {
    font-family: 'Manrope', sans-serif;
    font-weight: 600; font-size: 1.1rem;
    color: #FFFFFF; margin-bottom: 0.1rem;
}

/* Sidebar Customisation */
[data-testid="stSidebar"] {
    background-color: #110D17 !important;
    border-right: 1px solid #2A1A4A;
}
.stRadio > div { gap: 1rem; }
.stRadio label {
    font-family: 'Manrope', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    color: #8E8D92 !important;
    cursor: pointer;
    padding: 0.2rem 0;
    transition: color 0.2s ease;
}
.stRadio label:hover { color: #B388FF !important; }

/* Elegant Input & Select Fields */
div[data-testid="stTextInput"] input, div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: #1A1525;
    border: 1px solid #2A1A4A;
    border-radius: 12px;
    color: white;
    transition: border 0.3s ease, box-shadow 0.3s ease;
}
div[data-testid="stTextInput"] input:focus, div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
    border: 1px solid #B388FF;
    box-shadow: 0 0 10px rgba(179, 136, 255, 0.2);
}
div[data-testid="stSelectbox"] label { display: none; }

/* Base Authenticated Action Buttons */
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #7E57C2 0%, #9C27B0 100%) !important;
    color: #FFFFFF !important;
    font-family: 'Manrope', sans-serif !important;
    font-weight: 700 !important; font-size: 0.9rem !important;
    border-radius: 12px !important; border: none !important;
    padding: 0.6rem 1.5rem !important;
    box-shadow: 0 4px 15px rgba(126,87,194,0.4) !important;
    transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
    width: 100%;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(126,87,194,0.6) !important;
    background: linear-gradient(135deg, #8E6CE2 0%, #BA47D1 100%) !important;
}

/* Login specific primary button */
[data-testid="stForm"] .stButton > button {
    background: linear-gradient(135deg, #D4E157 0%, #AEEA00 100%) !important;
    color: #110D17 !important;
    box-shadow: 0 4px 15px rgba(212,225,87,0.3) !important;
}
[data-testid="stForm"] .stButton > button:hover {
    box-shadow: 0 8px 25px rgba(212,225,87,0.5) !important;
}

.insight-box {
    background: linear-gradient(135deg, #1A1525 0%, #2A1A4A 100%);
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid #3B2D59;
    margin-bottom: 2rem;
    transition: all 0.3s ease;
}
.insight-box:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    border-color: #D4E157;
}
.insight-box h4 {
    font-family: 'Manrope', sans-serif;
    color: #D4E157;
    margin: 0 0 0.5rem 0;
    font-size: 1rem;
}
.insight-box p {
    color: #EEEDEB;
    line-height: 1.6;
    margin: 0;
    font-size: 0.9rem;
}

/* Page titles */
.page-header {
    font-family: 'Manrope', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 1.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #2A1A4A;
}

/* History Logs */
.log-row {
    display: flex; justify-content: space-between; align-items: center;
    background: #1A1525; border: 1px solid #2A1A4A; 
    border-radius: 12px; padding: 1rem; margin-bottom: 0.8rem;
    transition: transform 0.2s;
}
.log-row:hover {
    transform: scale(1.01);
    border-color: #B388FF;
}
</style>""", unsafe_allow_html=True)


# ==============================================================================
# AUTHENTICATION ROUTING
# ==============================================================================

if not st.session_state.logged_in:
    # ---------------- LOGIN PAGE ----------------
    
    # Hide sidebar when logged out
    st.markdown("""<style>[data-testid="stSidebar"] { display: none; }</style>""", unsafe_allow_html=True)
    
    colA, colB, colC = st.columns([1, 1.5, 1])
    with colB:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        # Authentic vector geometry logo
        st.markdown("""
        <div style='margin: 0 auto 1.5rem auto; width: 64px; height: 64px;'>
            <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <defs><linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#B388FF;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#7E57C2;stop-opacity:1" />
                </linearGradient></defs>
                <circle cx="40" cy="40" r="30" fill="url(#grad)" opacity="0.8"/>
                <circle cx="60" cy="60" r="30" fill="#D4E157" opacity="0.9"/>
                <circle cx="50" cy="50" r="15" fill="#15111B"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<p class='login-title'>nix<span style='color:#B388FF'>tio</span></p>", unsafe_allow_html=True)
        st.markdown("<p class='login-subtitle'>Intelligence System Login</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="admin")
            password = st.text_input("Password", type="password", placeholder="admin123")
            submitted = st.form_submit_button("Authenticate Security")
            
            if submitted:
                if username == "admin" and password == "admin123":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
        
        st.markdown("<p style='font-size:0.75rem; color:#8E8D92; margin-top:2rem'>Demo pass: admin / admin123</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
else:
    # ---------------- MAIN APPLICATION ----------------
    
    # Cached data loaders
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

    @st.cache_data(ttl=3600, show_spinner=False)
    def cached_review_sentiment(sector_key: str) -> dict:
        return get_review_sentiment(SECTORS[sector_key].get("app_ids", {}))

    def apply_layout(fig, height=350):
        fig.update_layout(
            title=None,
            font=dict(family="Inter, sans-serif", size=11, color="#8E8D92"),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=30, r=20, t=10, b=30), height=height,
            xaxis=dict(showgrid=False, linecolor="#2A1A4A", gridcolor="#2A1A4A"),
            yaxis=dict(showgrid=True, gridcolor="#2A1A4A", gridwidth=1, linecolor="#2A1A4A"),
            legend=dict(font=dict(family="Inter", size=11, color="#EEEDEB"), bgcolor="rgba(0,0,0,0)", orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            hoverlabel=dict(bgcolor="#15111B", font_size=12, font_family="Inter", bordercolor="#B388FF", font_color="white"),
        )
        return fig

    def color_map_for(companies):
        return {c: CHART_COLORS[i % len(CHART_COLORS)] for i, c in enumerate(companies)}


    # Navigation Sidebar
    with st.sidebar:
        # Authentic SVG text/icon logo
        st.markdown("""
        <div style='padding:1rem 0 2rem 0; display:flex; align-items:center; gap: 10px'>
            <svg width="32" height="32" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <circle cx="40" cy="40" r="30" fill="#B388FF" opacity="0.8"/>
                <circle cx="60" cy="60" r="30" fill="#D4E157" opacity="0.9"/>
            </svg>
            <div>
                <h2 style='margin:0;font-family:Manrope,sans-serif;font-weight:800;color:#B388FF; line-height:1'>nix<span style='color:#FFF'>tio</span></h2>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        view = st.radio("MENU", [
            "Overview", 
            "Brand Dashboard", 
            "Talent Pool & CX", 
            "Generate Report", 
            "Report History", 
            "About Product"
        ])
        
        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        st.sidebar.markdown("---")
        st.sidebar.markdown("**Compare mode**")
        enable_compare = False
        company_a = None
        company_b = None
        
        enable_compare = st.sidebar.toggle("Enable comparison", value=False)
        if enable_compare:
            if view not in ["Report History", "About Product"]:
                from data.sectors import SECTORS, list_sector_keys
                # Safe access to selected sector before rendering
                curr_sector = st.session_state.get("sector_selector", list_sector_keys()[0])
                companies_list = SECTORS.get(curr_sector, SECTORS[list_sector_keys()[0]])["companies"]
                company_a = st.sidebar.selectbox("Company A", companies_list, key="cmp_a")
                company_b = st.sidebar.selectbox("Company B", 
                                [c for c in companies_list if c != company_a], key="cmp_b")
            else:
                st.sidebar.warning("Select a dashboard view to compare.")

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#8E8D92;font-size:0.75rem;'>System Time:<br><span style='color:#D4E157'>{timestamp_label()}</span></p>", unsafe_allow_html=True)
        
        # Logout button
        if st.button("Logout Session"):
            st.session_state.logged_in = False
            st.rerun()

    # Top Bar (Header)
    top1, top2, top3 = st.columns([4, 3, 3])

    with top1:
        st.markdown(f"<p class='dashboard-title'>{view}</p>", unsafe_allow_html=True)

    with top2:
        if view not in ["Report History", "About Product"]:
            selected_sector = st.selectbox("Sector", list_sector_keys(), index=0, key="sector_selector")
        else:
            selected_sector = "None"

    with top3:
        # Admin Profile Mrinmoy Banikya
        st.markdown("""
        <div style='display:flex; justify-content:flex-end; align-items:center; height:100%; gap: 12px;'>
            <div style='text-align:right'>
                <div style='font-family:Manrope; font-weight:700; font-size:0.95rem; color:#FFF'>Mrinmoy Banikya</div>
                <div style='font-family:Inter; font-size:0.7rem; color:#D4E157; font-weight:600; text-transform:uppercase; letter-spacing:0.05em'>Super Admin</div>
            </div>
            <div style='width:42px;height:42px;border-radius:50%;background:linear-gradient(135deg, #B388FF, #7E57C2);display:flex;align-items:center;justify-content:center;color:#FFF;font-weight:bold;font-size:1.2rem;box-shadow: 0 4px 10px rgba(126,87,194,0.4)'>M</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------------------------
    # Global Data Loading 
    # ---------------------------------------------------------------------------
    
    if view not in ["Report History", "About Product"]:
        sector_config = SECTORS[selected_sector]
        companies = sector_config["companies"]
        cmap = color_map_for(companies)

        with st.spinner("Syncing intelligence data..."):
            ratings_data = cached_playstore_ratings(selected_sector)
            trends_df    = cached_google_trends(selected_sector)
            news_data    = cached_news_mentions(selected_sector, NEWS_API_KEY)
            jobs_data    = cached_linkedin_jobs(selected_sector)
            employer_data = cached_ambitionbox(selected_sector)
            sentiment_data = cached_review_sentiment(selected_sector)

        with st.sidebar:
            from components.analyst_chat import render_analyst_sidebar
            data = {
                "ratings": ratings_data,
                "jobs": jobs_data,
                "news": news_data,
                "glassdoor": employer_data
            }
            meta = SECTOR_META.get(selected_sector, {})
            render_analyst_sidebar(selected_sector, companies, data, meta)

    # ---------------------------------------------------------------------------
    # Routing Views
    # ---------------------------------------------------------------------------

    if enable_compare and view not in ["Report History", "About Product"]:
        if company_a and company_b:
            from components.comparison import render_comparison
            render_comparison(company_a, company_b, ratings_data, jobs_data, news_data, employer_data, trends_df)
            st.stop()

    if view == "Overview":
        rv = [v["rating"] for v in ratings_data.values() if v["rating"] > 0] if ratings_data else []
        avg_rating = round(sum(rv) / len(rv), 1) if rv else 0.0
        top_hire_co = max(jobs_data, key=jobs_data.get) if jobs_data else "N/A"
        top_hire_n  = jobs_data[top_hire_co] if jobs_data else 0
        total_news = sum(news_data.values()) if news_data else 0

        # --- Executive Summary Calculation ---
        # Line 1: Momentum
        brand_lead = "N/A"
        trends_last = 0.0
        pct_above_avg = 0.0
        if not trends_df.empty:
            lasts = {}
            for co in companies:
                if co in trends_df.columns:
                    try: lasts[co] = float(trends_df[co].iloc[-1])
                    except: pass
            if lasts:
                brand_lead = max(lasts, key=lasts.get)
                trends_last = lasts[brand_lead]
                avg_trends = sum(lasts.values()) / len(lasts)
                pct_above_avg = ((trends_last - avg_trends) / avg_trends * 100) if avg_trends > 0 else 0

        # Line 2: Talent
        avg_jobs = sum(jobs_data.values()) / len(jobs_data) if jobs_data else 1
        pct_diff = ((top_hire_n - avg_jobs) / avg_jobs * 100) if avg_jobs > 0 else 0

        # Line 3: Risk
        max_j = max(jobs_data.values()) if jobs_data and any(jobs_data.values()) else 1
        risk_co = max(companies, key=lambda c: (jobs_data.get(c, 0)/max_j) - (employer_data.get(c, 5.0)/5.0))
        risk_jobs = jobs_data.get(risk_co, 0)
        risk_emp = employer_data.get(risk_co, 0.0)

        line1 = f"{brand_lead} is the dominant brand in {selected_sector} with a Google Trends index of {trends_last:.0f}/100 — {pct_above_avg:.0f}% above sector average."
        line2 = f"{top_hire_co} is in aggressive hiring mode with {top_hire_n} open roles ({pct_diff:+.0f}% vs sector avg) — watch for a product launch signal."
        line3 = f"{risk_co} shows scaling stress: {risk_jobs} open roles but only {risk_emp:.1f}/5 employer rating — attrition risk is elevated."

        st.markdown(f"""
        <div style="font-size: 10px; color: #378ADD; font-weight: bold; letter-spacing: 1px; margin-bottom: 8px;">EXECUTIVE SUMMARY</div>
        <div style="background: #0D1117; border: 1px solid #21262D; border-radius: 12px; padding: 16px 20px; color: #B3D4F5; font-size: 13px; display: flex; flex-direction: column; gap: 10px; margin-bottom: 1.5rem;">
            <div style="background: rgba(255,255,255,0.03); border-radius: 20px; padding: 10px 16px;"><span style='color: #008080; margin-right: 8px; font-size:16px;'>●</span> {line1}</div>
            <div style="background: rgba(255,255,255,0.03); border-radius: 20px; padding: 10px 16px;"><span style='color: #378ADD; margin-right: 8px; font-size:16px;'>●</span> {line2}</div>
            <div style="background: rgba(255,255,255,0.03); border-radius: 20px; padding: 10px 16px;"><span style='color: #FFB74D; margin-right: 8px; font-size:16px;'>●</span> {line3}</div>
        </div>
        """, unsafe_allow_html=True)

        # --- Sector Intelligence ---
        st.markdown("<p class='chart-title'>Sector Intelligence</p>", unsafe_allow_html=True)
        if selected_sector in SECTOR_META:
            meta = SECTOR_META[selected_sector]
            
            # 4 metric cards
            mi1, mi2, mi3, mi4 = st.columns([1,1,1,1])
            with mi1:
                with st.container(border=True):
                    st.metric("TAM", f"${meta['tam_usd_bn']}Bn")
            with mi2:
                with st.container(border=True):
                    st.metric("CAGR", f"{meta['cagr_pct']}%")
            with mi3:
                with st.container(border=True):
                    st.metric("Saturation", f"{meta['saturation_score']}/100")
            with mi4:
                with st.container(border=True):
                    st.metric("Stage", meta['market_stage'])
            
            # 3 columns for lists
            tl1, tl2, tl3 = st.columns([1,1,1])
            with tl1:
                st.markdown("**Tailwinds**")
                for tw in meta['key_tailwinds']:
                    st.markdown(f"- {tw}")
            with tl2:
                st.markdown("**Unsolved Problems**")
                for up in meta['unsolved_problems']:
                    st.markdown(f"- {up}")
            with tl3:
                st.markdown("**Sector Risks**")
                for sr in meta['sector_risks']:
                    st.markdown(f"- {sr}")
            
            # --- Sector Opportunity Radar ---
            st.markdown("#### Sector Opportunity Radar")
            radar = meta.get("radar", {})
            categories = ["Saturation", "Capital Intensity", "Talent Scarcity", 
                          "Regulatory Risk", "Consumer Demand", "White Space Opp."]
            values = [
                radar.get("saturation", 50),
                radar.get("capital_intensity", 50),
                radar.get("talent_scarcity", 50),
                radar.get("regulatory_risk", 50),
                radar.get("consumer_demand", 50),
                radar.get("white_space", 50),
            ]
            values_closed = values + [values[0]]
            categories_closed = categories + [categories[0]]
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values_closed,
                theta=categories_closed,
                fill='toself',
                fillcolor='rgba(55,138,221,0.15)',
                line=dict(color='#378ADD', width=2),
                name=selected_sector
            ))
            fig.update_layout(
                polar=dict(
                    bgcolor='#0D1117',
                    radialaxis=dict(visible=True, range=[0,100], 
                                   gridcolor='#21262D', tickcolor='#21262D',
                                   tickfont=dict(color='#8B949E', size=9)),
                    angularaxis=dict(gridcolor='#21262D', 
                                    tickfont=dict(color='#E6EDF3', size=11))
                ),
                paper_bgcolor='#161B22',
                plot_bgcolor='#161B22',
                showlegend=False,
                height=380,
                margin=dict(l=60, r=60, t=40, b=40)
            )
            
            col_radar, col_radar_text = st.columns([1, 1])
            with col_radar:
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            with col_radar_text:
                st.markdown("**Reading the radar**")
                for cat, val in zip(categories, values):
                    color = "#3FB950" if val < 40 else ("#D29922" if val < 70 else "#F85149")
                    st.markdown(f"""
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 4px;">
                        <span style="font-size:12px; color:#8B949E;">{cat}</span>
                        <span style="font-size:12px; font-weight:bold; color:{color};">{val}/100</span>
                    </div>
                    <div style="width:100%; height:6px; background:#21262D; border-radius:3px; margin-bottom:12px;">
                        <div style="width:{val}%; height:100%; border-radius:3px; background:{color};"></div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style='border-left: 3px solid #378ADD; padding-left: 12px; margin-top: 16px; font-size: 13px; color: #E6EDF3;'>
                    {meta.get('radar_insight','Strategic pattern analysis unavailable.')}
                </div>
                """, unsafe_allow_html=True)

            # Reddit Signal Card
            reddit_pts = "".join([f"<div style='border-left: 2px solid #FF4500; background: #1A1A1A; padding: 10px; margin-bottom: 8px; border-radius: 4px; color: #EEEDEB; font-size: 13px;'>{pt}</div>" for pt in meta['reddit_pain_points']])
            
            st.markdown(f"""
            <div style="background: #161B22; border: 1px solid #21262D; border-radius: 12px; padding: 16px 20px; margin-top: 1rem; margin-bottom: 1.5rem;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                    <svg width="24" height="24" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="50" cy="50" r="50" fill="#FF4500"/>
                        <text x="50" y="70" font-family="Arial, sans-serif" font-weight="bold" font-size="60" fill="white" text-anchor="middle">R</text>
                    </svg>
                    <span style="font-family: 'Manrope', sans-serif; font-weight: 700; font-size: 1.1rem; color: #FFFFFF;">Reddit Signal</span>
                </div>
                {reddit_pts}
            </div>
            """, unsafe_allow_html=True)

            if st.button("View All Players in Sector", type="secondary"):
                st.session_state["show_players"] = not st.session_state.get("show_players", False)
                st.rerun()
                
            if st.session_state.get("show_players", False):
                with st.container():
                    st.markdown("### Sector Player Map")
                    players = meta.get("players", {})
                    tiers = ["public_companies", "private_giants", "rising_startups"]
                    tier_labels = {"public_companies": "Public Companies", 
                                   "private_giants": "Private Giants (>$500M)", 
                                   "rising_startups": "Rising Startups (<$500M)"}
                    tier_colors = {"public_companies": "#1D9E75", 
                                   "private_giants": "#378ADD", 
                                   "rising_startups": "#D85A30"}
                    
                    for tier in tiers:
                        tier_players = players.get(tier, [])
                        if not tier_players:
                            continue
                        st.markdown(f"<p style='border-left: 4px solid {tier_colors[tier]}; padding-left: 8px; font-family: Manrope; font-weight: 700; margin-top: 1.5rem;'>{tier_labels[tier]}</p>", unsafe_allow_html=True)
                        
                        cols = st.columns(max(min(len(tier_players), 4), 1))
                        for idx, p in enumerate(tier_players):
                            with cols[idx % 4]:
                                with st.container(border=True):
                                    st.markdown(f"**{p['name']}**")
                                    val_str = f"${p.get('market_cap_usd_bn') or p.get('valuation_usd_bn')}Bn" if (p.get('market_cap_usd_bn') or p.get('valuation_usd_bn')) else "Undisclosed"
                                    st.markdown(f"Valuation: {val_str}")
                                    stage = p.get('stage', 'Public')
                                    st.markdown(f"Stage: <span style='color:{tier_colors[tier]}'>{stage}</span>", unsafe_allow_html=True)
                                    st.markdown(f"HQ: {p.get('hq', 'Unknown')}")
                                    if st.button(f"Deep Dive: {p['name']}", key=f"dd_{tier}_{p['name']}"):
                                        st.session_state["selected_company"] = p['name']
                                        st.rerun()
            
            if st.session_state.get("selected_company"):
                try:
                    from components.company_drawer import render_company_drawer
                    all_data = {
                        "ratings": ratings_data,
                        "trends": trends_df,
                        "news": news_data,
                        "jobs": jobs_data,
                        "employer": employer_data,
                        "sentiment": sentiment_data
                    }
                    render_company_drawer(st.session_state["selected_company"], selected_sector, all_data)
                except ImportError:
                    st.warning("Company drawer component not yet integrated.")

        m1, m2, m3 = st.columns(3)
        with m1:
            with st.container(border=True):
                st.metric("Sector App Avg", f"{avg_rating} \u2605" if avg_rating else "N/A", delta="Play Store")
        with m2:
            with st.container(border=True):
                st.metric("Top Recruiter", top_hire_co, delta=f"{top_hire_n} open roles")
        with m3:
            with st.container(border=True):
                st.metric("News Mentions (30d)", format_large_number(total_news) if total_news else "N/A", delta="Total sector visibility")
                
        # --- Company Health Scorecard ---
        import random
        max_jobs = max(list(jobs_data.values()) + [1]) if jobs_data else 1
        max_news = max(list(news_data.values()) + [1]) if news_data else 1
        
        score_data = []
        for co in companies:
            app_s = (ratings_data.get(co, {}).get("rating", 0) / 5.0) * 25
            hire_s = min((jobs_data.get(co, 0) / max_jobs) * 25, 25)
            
            brand_val = 0
            if not trends_df.empty and co in trends_df.columns:
                try: brand_val = float(trends_df[co].iloc[-1])
                except: pass
            brand_s = (brand_val / 100) * 20
            
            news_s = min((news_data.get(co, 0) / max_news) * 15, 15)
            
            emp_val = employer_data.get(co, 1.0)
            if emp_val < 1: emp_val = 1.0
            emp_s = ((emp_val - 1) / 4) * 15
            
            overall = round(app_s + hire_s + brand_s + news_s + emp_s, 1)
            
            rng = random.Random(co)
            trend_val = rng.choice(["Up ⬆", "Flat ➖", "Down ⬇"])
            
            score_data.append({
                "Company": co,
                "Overall Score": overall,
                "App": round(app_s, 1),
                "Hiring": round(hire_s, 1),
                "Brand": round(brand_s, 1),
                "News": round(news_s, 1),
                "Employer": round(emp_s, 1),
                "Trend": trend_val
            })
            
        score_df = pd.DataFrame(score_data).sort_values("Overall Score", ascending=False).reset_index(drop=True)
        score_df.index = score_df.index + 1
        score_df = score_df.reset_index().rename(columns={"index": "Rank"})
        
        def color_overall_score(val):
            if val >= 70: color = '#81C784'
            elif val >= 50: color = '#FFB74D'
            else: color = '#E57373'
            return f'color: {color}; font-weight: bold;'
            
        styled_df = score_df.style.map(color_overall_score, subset=['Overall Score'])
        
        st.markdown("<p class='chart-title'>Company Health Scorecard</p>", unsafe_allow_html=True)
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        st.caption("Composite score across product, talent, brand, press and employer dimensions.")
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class='insight-box'>
            <h4>💡 Analyst Momentum Insight</h4>
            <p>{sector_config["insight"]}</p>
        </div>""", unsafe_allow_html=True)

        # --- Competitive Positioning Matrix ---
        scatter_data = []
        for co in companies:
            x_val = 0
            if not trends_df.empty and co in trends_df.columns:
                try:
                    x_val = float(trends_df[co].iloc[-1])
                except:
                    pass
            
            y_val = 0
            if ratings_data and co in ratings_data:
                y_val = (ratings_data[co].get("rating", 0) / 5) * 100
                
            size = jobs_data.get(co, 0) if jobs_data else 0
            
            scatter_data.append({
                "Company": co,
                "Brand Momentum": x_val,
                "Product Score": y_val,
                "Open Roles": max(size, 5),
                "Jobs": size
            })
            
        sdf = pd.DataFrame(scatter_data)
        
        st.markdown("<p class='chart-title'>Competitive Positioning Matrix</p>", unsafe_allow_html=True)
        st.markdown("<p class='chart-subtitle'>Bubble size = hiring velocity &nbsp;|&nbsp; X = brand momentum &nbsp;|&nbsp; Y = product quality</p>", unsafe_allow_html=True)
        with st.container(border=True):
            fig_scatter = px.scatter(
                sdf, x="Brand Momentum", y="Product Score", size="Open Roles",
                color="Company", color_discrete_map=cmap, text="Company",
                hover_data={"Jobs": True, "Open Roles": False}
            )
            
            fig_scatter.add_vline(x=50, line_dash="dash", line_color="#2A1A4A", opacity=0.7)
            fig_scatter.add_hline(y=50, line_dash="dash", line_color="#2A1A4A", opacity=0.7)
            
            # Quadrant Labels
            fig_scatter.add_annotation(x=98, y=98, text="<b>Leaders</b>", showarrow=False, font=dict(color="#81C784", size=14), xanchor="right", yanchor="top")
            fig_scatter.add_annotation(x=2, y=98, text="<b>Hidden gems</b>", showarrow=False, font=dict(color="#B388FF", size=14), xanchor="left", yanchor="top")
            fig_scatter.add_annotation(x=98, y=2, text="<b>Hype vs reality</b>", showarrow=False, font=dict(color="#FFB74D", size=14), xanchor="right", yanchor="bottom")
            fig_scatter.add_annotation(x=2, y=2, text="<b>Watch list</b>", showarrow=False, font=dict(color="#E57373", size=14), xanchor="left", yanchor="bottom")
            
            fig_scatter.update_traces(
                textposition="top center", 
                textfont=dict(family="Inter", size=11, color="#EEEDEB"),
                marker=dict(sizemin=4, line=dict(width=1.5, color="#15111B"))
            )
            fig_scatter.update_xaxes(range=[-5, 105])
            fig_scatter.update_yaxes(range=[-5, 105])
            
            apply_layout(fig_scatter, 450)
            fig_scatter.update_layout(showlegend=False)
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        st.markdown("<br>", unsafe_allow_html=True)

        # --- Funding Landscape ---
        funding_dict = sector_config.get("funding", {})
        if funding_dict:
            st.markdown("<p class='chart-title'>Funding Landscape</p>", unsafe_allow_html=True)
            
            funding_data = []
            for co in companies:
                if co in funding_dict:
                    f = funding_dict[co]
                    funding_data.append({
                        "Company": co,
                        "Last Round": f.get("last_round", ""),
                        "Amount ($M)": f.get("amount_usd_m", 0),
                        "Year": f.get("year", ""),
                        "Total Raised ($M)": f.get("total_raised_usd_m", 0),
                        "Valuation Tier": f.get("valuation_tier", "")
                    })
            
            if funding_data:
                fdf = pd.DataFrame(funding_data)
                total_sector_raised_m = fdf["Total Raised ($M)"].sum()
                total_sector_raised_bn = total_sector_raised_m / 1000.0
                
                with st.container(border=True):
                    st.metric("Total sector capital raised", f"${total_sector_raised_bn:.2f} Bn")
                    
                    fdf_sorted = fdf.sort_values("Total Raised ($M)", ascending=True)
                    tier_colors = {
                        "Bootstrapped": "#9E9E9E",
                        "Growth": "#81C784",
                        "Soonicorn": "#FFB74D",
                        "Unicorn": "#B388FF",
                        "Public": "#378ADD",
                        "Private Enterprise": "#5C6BC0"
                    }
                    
                    fig_fund = px.bar(
                        fdf_sorted, x="Total Raised ($M)", y="Company", 
                        color="Valuation Tier", color_discrete_map=tier_colors,
                        orientation="h", text="Total Raised ($M)"
                    )
                    fig_fund.update_traces(textposition="outside", textfont=dict(color="#FFF"), marker_cornerradius=8)
                    apply_layout(fig_fund, 350)
                    st.plotly_chart(fig_fund, use_container_width=True)
                    
                    st.markdown("<p class='chart-subtitle' style='margin-top:1rem; margin-bottom:0.5rem;'>Cap Table & Latest Round Details</p>", unsafe_allow_html=True)
                    display_fdf = fdf.drop(columns=["Total Raised ($M)"]).sort_values("Amount ($M)", ascending=False).set_index("Company")
                    st.dataframe(display_fdf, use_container_width=True)
                    
            st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<p class='chart-title'>Search Interest Over Time</p>", unsafe_allow_html=True)
        with st.container(border=True):
            if not trends_df.empty:
                tdf = trends_df.drop(columns=["isPartial"], errors="ignore").reset_index()
                date_col = tdf.columns[0]
                val_cols = [c for c in tdf.columns if c != date_col]
                long = tdf.melt(id_vars=[date_col], value_vars=val_cols, var_name="Company", value_name="Interest")
                fig3 = px.line(long, x=date_col, y="Interest", color="Company", color_discrete_map=cmap)
                fig3.update_traces(line=dict(width=3, shape="spline"), mode="lines")
                apply_layout(fig3, 300)
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("Google Trends data unavailable.")

        # --- Analyst Intelligence Memo ---
        st.markdown("<br><p class='chart-title'>Analyst Intelligence Memo</p>", unsafe_allow_html=True)
        
        memo_key = f"memo_{selected_sector}"
        
        if st.button("Generate AI Memo"):
            with st.spinner("Compiling strategic intelligence..."):
                try:
                    import anthropic
                    from datetime import datetime
                    
                    # Compute dynamic metrics for the prompt
                    brand_leader = "N/A"
                    if not trends_df.empty:
                        lasts = []
                        for co in companies:
                            if co in trends_df.columns:
                                try:
                                    lasts.append((co, float(trends_df[co].iloc[-1])))
                                except: pass
                        if lasts:
                            brand_leader = max(lasts, key=lambda x: x[1])[0]

                    user_prompt = f"""
Sector: {selected_sector}
Companies: {', '.join(companies)}
Top hiring company: {top_hire_co} with {top_hire_n} open roles
Brand leader: {brand_leader}
App ratings: {ratings_data}
News mentions: {news_data}
Employer scores: {employer_data}

Write a 3-paragraph analyst memo:
Para 1: What is the single most important strategic signal in this data?
Para 2: Which company is best positioned for the next 12 months and why?
Para 3: What should the reader's company specifically watch out for?

Keep each paragraph to 3 sentences max. Start each with a bold headline.
"""
                    anthropic_api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
                    if not anthropic_api_key or "paste_" in anthropic_api_key:
                        raise ValueError("Valid ANTHROPIC_API_KEY is missing from .streamlit/secrets.toml")
                        
                    client = anthropic.Anthropic(api_key=anthropic_api_key)
                    
                    response = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        system="You are a senior strategy analyst at a top-tier consulting firm. Write in crisp, executive language. No fluff. Short paragraphs.",
                        messages=[{"role": "user", "content": user_prompt}],
                        max_tokens=800
                    )
                    
                    import datetime
                    st.session_state[memo_key] = {
                        "content": response.content[0].text,
                        "timestamp": datetime.datetime.now().strftime("%B %d, %Y - %H:%M")
                    }
                except Exception as e:
                    st.error(f"AI Memo generation failed: {e}")
                    
        if memo_key in st.session_state:
            memo_data = st.session_state[memo_key]
            # Replace newlines with <br> for HTML rendering, or just use markdown directly!
            # Since st.markdown allows both markdown syntax and HTML, let's wrap it in a container
            st.markdown(f"""
            <div style='border-left: 4px solid #378ADD; background: rgba(55,138,221,0.05); padding: 1.5rem; border-radius: 4px; margin-top: 1rem; font-family: Inter, sans-serif; font-size: 0.95rem; line-height: 1.6; color: #EEEDEB;'>
                {memo_data["content"].replace(chr(10), "<br>")}
            </div>
            <div style='font-size: 0.8rem; color: #8E8D92; margin-top: 0.5rem; text-align: right;'>
                Last updated: {memo_data["timestamp"]}
            </div>
            """, unsafe_allow_html=True)


    elif view == "Brand Dashboard":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<p class='chart-title'>News Mentions (Past 30 Days)</p>", unsafe_allow_html=True)
            with st.container(border=True):
                if news_data and any(v > 0 for v in news_data.values()):
                    ndf = pd.DataFrame([{"Company": k, "Mentions": v} for k, v in news_data.items()]).sort_values("Mentions", ascending=True)
                    fig_news = px.bar(ndf, x="Mentions", y="Company", color="Company", color_discrete_map=cmap, orientation="h", text="Mentions")
                    fig_news.update_traces(textposition="outside", textfont=dict(color="#FFF"), marker_cornerradius=8)
                    apply_layout(fig_news, 400)
                    fig_news.update_layout(showlegend=False)
                    st.plotly_chart(fig_news, use_container_width=True)
                else:
                    st.info("No news data.")
        with c2:
            st.markdown("<p class='chart-title'>Brand Interest Distribution</p>", unsafe_allow_html=True)
            with st.container(border=True):
                if not trends_df.empty:
                    tcols = [c for c in trends_df.columns if c not in ("date", "isPartial")]
                    avgs = trends_df[tcols].mean().reset_index()
                    avgs.columns = ["Company", "Avg Interest"]
                    fig_pie = px.pie(avgs, names="Company", values="Avg Interest", color="Company", color_discrete_map=cmap, hole=0.6)
                    fig_pie.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#15111B', width=2)))
                    fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10, l=10, r=10), showlegend=False, height=400)
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("No trend data.")


    elif view == "Talent Pool & CX":
        colA, colB = st.columns([1, 1])
        with colA:
            st.markdown("<p class='chart-title'>Hiring Velocity</p>", unsafe_allow_html=True)
            with st.container(border=True):
                if jobs_data and any(v > 0 for v in jobs_data.values()):
                    jdf = pd.DataFrame([{"Company": k, "Open Roles": v} for k, v in jobs_data.items()]).sort_values("Open Roles", ascending=False)
                    fig2 = px.bar(jdf, x="Company", y="Open Roles", color="Company", color_discrete_map=cmap, text="Open Roles")
                    fig2.update_traces(textposition="outside", textfont=dict(color="#FFF"), marker_cornerradius=8)
                    apply_layout(fig2, 350)
                    fig2.update_layout(showlegend=False)
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.info("No hiring data.")
        with colB:
            st.markdown("<p class='chart-title'>CSAT & App Ratings</p>", unsafe_allow_html=True)
            with st.container(border=True):
                if ratings_data:
                    rdf = pd.DataFrame([{"Company": k, "Rating": v["rating"]} for k, v in ratings_data.items() if v["rating"] > 0])
                    if not rdf.empty:
                        fig1 = px.bar(rdf, x="Company", y="Rating", color="Company", color_discrete_map=cmap, text="Rating")
                        fig1.update_traces(textposition="outside", textfont=dict(color="#FFF"), width=0.5, marker_cornerradius=8)
                        fig1.update_yaxes(range=[0, 5])
                        apply_layout(fig1, 350)
                        fig1.update_layout(showlegend=False)
                        st.plotly_chart(fig1, use_container_width=True)
                    else:
                        st.info("No ratings.")
                else:
                    st.info("No ratings.")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- Review Sentiment Analysis ---
        st.markdown("<p class='chart-title'>Review Sentiment</p>", unsafe_allow_html=True)
        if sentiment_data:
            s_list = []
            for co, v in sentiment_data.items():
                if v["review_count"] > 0:
                    s_list.append({"Company": co, "Sentiment": "Positive", "Percentage": v["positive_pct"]})
                    s_list.append({"Company": co, "Sentiment": "Neutral", "Percentage": v["neutral_pct"]})
                    s_list.append({"Company": co, "Sentiment": "Negative", "Percentage": v["negative_pct"]})
            
            if s_list:
                with st.container(border=True):
                    sdf = pd.DataFrame(s_list)
                    color_m = {"Positive": "#81C784", "Neutral": "#9E9E9E", "Negative": "#E57373"}
                    fig_s = px.bar(sdf, y="Company", x="Percentage", color="Sentiment", 
                                   orientation='h', barmode='stack', color_discrete_map=color_m)
                    apply_layout(fig_s, max(250, len(sentiment_data)*60))
                    fig_s.update_traces(marker_cornerradius=0)
                    # Show legend at the top
                    fig_s.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title=None))
                    st.plotly_chart(fig_s, use_container_width=True)
                    
                    st.markdown("<div style='display:flex; flex-wrap:wrap; gap:20px; align-items:flex-start; margin-top:10px'>", unsafe_allow_html=True)
                    for co in sentiment_data:
                        if sentiment_data[co]["review_count"] > 0:
                            v = sentiment_data[co]
                            pills = "".join([f"<span style='background:#E57373; padding:2px 8px; border-radius:12px; font-size:0.75rem; color:#1A1A1A; font-family:Inter; font-weight:600; margin-right:4px;'>{w}</span>" for w in v["top_complaints"][:3]])
                            st.markdown(f"<div><span style='color:#EEEDEB; font-family:Inter; font-size:0.85rem; font-weight:600; margin-bottom:4px; display:inline-block'>🚨 {co} Complaints:</span><br>{pills}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.caption("Based on top 100 most relevant Play Store reviews")
            else:
                st.info("No sentiment data generated.")
        else:
            st.info("No Play Store apps available for this sector to analyse.")


    elif view == "Generate Report":
        st.markdown("""
            <p style='color:#8E8D92; font-size:1.1rem; max-width:800px'>Compile latest intelligence, search momentum, 
            and talent velocity into a fully annotated executive PDF report.</p>
        """, unsafe_allow_html=True)
        
        left, right = st.columns([1, 2])
        with left:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📄 Generate Intelligence Report"):
                with st.spinner("Generating High-Resolution PDF..."):
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
                            personalised_line_1=f"{companies[0]} shows dynamic movement in {selected_sector}." if companies else "",
                            personalised_line_2=sector_config["insight"],
                            meta=SECTOR_META.get(selected_sector, {}),
                        )
                        if pdf_bytes:
                            # Log to history
                            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            st.session_state.history.append({"time": ts, "sector": selected_sector, "type": "PDF Report"})
                            
                            st.download_button(
                                "⬇ Proceed to Download",
                                data=pdf_bytes,
                                file_name=f"{selected_sector.lower().replace(' ', '_')}_report.pdf",
                                mime="application/pdf"
                            )
                        else:
                            st.warning("Empty output.")
                    except Exception as e:
                        st.error(f"PDF generation failed: {e}")
                        st.info("Dependencies: fpdf2 and kaleido must be installed.")


    elif view == "Report History":
        st.markdown("<div class='page-header'>Exported Reports History</div>", unsafe_allow_html=True)
        history = st.session_state.history
        
        if len(history) == 0:
            st.info("No reports generated during this session.")
        else:
            for item in reversed(history):
                st.markdown(f"""
                <div class='log-row'>
                    <div>
                        <span style='font-family:Manrope; font-weight:700'>{item['sector']}</span>
                        <div style='font-size:0.8rem; color:#8E8D92'>{item['type']}</div>
                    </div>
                    <div style='color:#D4E157; font-family:Inter; font-size:0.85rem'>{item['time']}</div>
                </div>
                """, unsafe_allow_html=True)


    elif view == "About Product":
        st.markdown("<div class='page-header'>About the Application</div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background:#15111B; border: 1px solid #2A1A4A; border-radius: 20px; padding: 2.5rem; text-align:center;'>
            <div style='margin: 0 auto 1rem auto; width: 80px; height: 80px;'>
                <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <defs><linearGradient id="g2" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#B388FF"/>
                        <stop offset="100%" style="stop-color:#7E57C2"/>
                    </linearGradient></defs>
                    <circle cx="40" cy="40" r="30" fill="url(#g2)" opacity="0.8"/>
                    <circle cx="60" cy="60" r="30" fill="#D4E157" opacity="0.9"/>
                    <circle cx="50" cy="50" r="15" fill="#15111B"/>
                </svg>
            </div>
            <h2 style='font-family:Manrope; color:#FFF; margin-bottom:0.5rem'>nix<span style='color:#B388FF'>tio</span> intelligence</h2>
            <p style='color:#8E8D92; max-width:600px; margin:0 auto; line-height:1.6'>
                An enterprise-grade competitive intelligence tracker compiling 
                market signals from Google Trends, LinkedIn Hiring Data, and Play Store Sentiment.
                Designed for high-performance executive analytics.
            </p>
            <br><br>
            <div style='display:inline-block; border-top: 1px solid #2A1A4A; padding-top:1.5rem'>
                <span style='color:#8E8D92; font-size:0.85rem'>Engineered & Managed by</span><br>
                <strong style='color:#FFF; font-size:1.1rem'>Mrinmoy Banikya</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

