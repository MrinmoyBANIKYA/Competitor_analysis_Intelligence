import streamlit as st
from groq import Groq
from data.company_profiles import COMPANY_PROFILES
from components.founder_panel import render_founder_panel

try:
    from data.reddit_signals import get_reddit_signals
except ImportError:
    def get_reddit_signals(term):
        return []

def render_company_drawer(company_name, sector_name, live_data):
    profile = COMPANY_PROFILES.get(company_name)
    if not profile:
        st.warning(f"No detailed profile found for {company_name}.")
        return

    # Fetch live data defaults
    ratings_dict = live_data.get("ratings", {})
    jobs_dict = live_data.get("jobs", {})
    news_dict = live_data.get("news", {})
    employer_dict = live_data.get("employer", {})  # Glassdoor / Ambitionbox

    app_rating = ratings_dict.get(company_name, {}).get("rating", 0.0) if ratings_dict else 0.0
    open_roles = jobs_dict.get(company_name, 0)
    news_mentions = news_dict.get(company_name, 0)
    employer_score = employer_dict.get(company_name, 1.0)

    # Calculate sector averages for deltas
    avg_rating = sum(r.get("rating", 0.0) for r in ratings_dict.values()) / max(len([r for r in ratings_dict.values() if r.get("rating", 0.0) > 0]), 1) if ratings_dict else 0.0
    avg_roles = sum(jobs_dict.values()) / max(len(jobs_dict), 1) if jobs_dict else 0.0
    avg_news = sum(news_dict.values()) / max(len(news_dict), 1) if news_dict else 0.0
    avg_emp_score = sum(employer_dict.values()) / max(len(employer_dict), 1) if employer_dict else 1.0

    with st.expander(f"Deep Dive: {company_name}", expanded=True):
        # SECTION 1: Identity
        c1, c2, c3, c4 = st.columns([2,1,1,1])
        with c1:
            st.markdown(f"<h2 style='margin-bottom:0; padding-bottom:0;'>{company_name}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#8E8D92; font-size:14px; margin-top:0;'>Founded {profile.get('founded')} • HQ: {profile.get('hq')}<br/>Founders: {', '.join(profile.get('founders', []))}</p>", unsafe_allow_html=True)
        with c2:
            val_str = f"${profile.get('valuation_usd_bn')}Bn" if profile.get('valuation_usd_bn') else "Undisclosed"
            st.metric("Valuation", val_str)
        with c3:
            amount = profile.get('last_round_amount_usd_m')
            st.metric("Last Round", profile.get("last_round", "N/A"), f"${amount}M" if amount else None)
        with c4:
            emp_cnt = profile.get('employee_count_approx')
            st.metric("Employees (Approx)", f"{emp_cnt:,}" if isinstance(emp_cnt, int) else str(emp_cnt))

        st.divider()

        # SECTION 2: ICP & Revenue
        icp_col, rev_col = st.columns(2)
        with icp_col:
            st.markdown("#### Ideal Customer Profile")
            st.markdown(f"**Target:** {profile.get('primary_customers')}")
            st.markdown(f"**Persona:** {profile.get('icp')}")
        with rev_col:
            st.markdown("#### Revenue Model & Products")
            st.markdown(f"**Model:** {profile.get('revenue_model')}")
            prods = "".join([f"<span style='background:#2A1A4A; color:#B388FF; padding:4px 8px; border-radius:12px; margin-right:6px; font-size:12px;'>{p}</span>" for p in profile.get('products', [])])
            st.markdown(f"<div style='margin-top:8px;'>{prods}</div>", unsafe_allow_html=True)

        st.divider()

        # SECTION 2.5: Leadership Intelligence
        render_founder_panel(company_name, profile)

        st.divider()

        # SECTION 3: Live Signals
        st.markdown("#### Live Intelligence Signals")
        s1, s2, s3, s4 = st.columns(4)
        with s1:
            st.metric("App Rating", f"{app_rating:.1f}" if app_rating else "N/A", f"{app_rating - avg_rating:+.1f} vs avg" if app_rating else None)
        with s2:
            st.metric("Open Roles", f"{open_roles}", f"{open_roles - avg_roles:+.0f} vs avg")
        with s3:
            st.metric("News Mentions 30D", f"{news_mentions}", f"{news_mentions - avg_news:+.0f} vs avg")
        with s4:
            st.metric("Employer Score", f"{employer_score:.1f}", f"{employer_score - avg_emp_score:+.1f} vs avg")

        st.write("")

        # SECTION 4: Known Gaps
        st.markdown("#### Known Product & Strategic Gaps")
        st.caption("Sourced from public reviews, analyst reports, and app store feedback")
        for gap in profile.get("known_gaps", []):
            st.markdown(f"""
            <div style='border-left: 4px solid #FFB74D; background: #1A1525; padding: 12px 16px; margin-bottom: 10px; border-radius: 4px;'>
                <span style='color: #FFB74D; font-weight: bold;'>Gap:</span> <span style='color: #EEEDEB;'>{gap}</span>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        # SECTION 5: Competitive Intelligence
        st.markdown("#### Competitive Intelligence")
        comp_col1, comp_col2 = st.columns(2)
        with comp_col1:
            st.markdown(f"""
            <div style='border: 1px solid #1D9E75; background: rgba(29, 158, 117, 0.1); padding: 16px; border-radius: 8px;'>
                <h5 style='color:#1D9E75; margin-top:0;'>Competitive Moat</h5>
                <span style='color:#EEEDEB;'>{profile.get('competitive_moat')}</span>
            </div>
            """, unsafe_allow_html=True)
        with comp_col2:
            threats = "".join([f"<span style='background:rgba(229, 115, 115, 0.1); color:#E57373; border: 1px solid #E57373; padding:4px 8px; border-radius:12px; margin-right:6px; font-size:12px; display:inline-block; margin-bottom:6px;'>⚠️ {t}</span>" for t in profile.get('threat_from', [])])
            st.markdown(f"""
            <div style='border: 1px solid #2A1A4A; background: #15111B; padding: 16px; border-radius: 8px; height: 100%;'>
                <h5 style='color:#E57373; margin-top:0;'>Threat From</h5>
                {threats}
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        # SECTION 6: Public Sentiment (Reddit)
        st.markdown("#### Pulse Check (Reddit & Twitter Signals)")
        try:
            reddit_quotes = get_reddit_signals(profile.get("reddit_search_term", company_name))
        except Exception:
            reddit_quotes = []

        if not reddit_quotes and profile.get("known_gaps"):
            reddit_quotes = [{"title": "Strategic Gap Identified", "snippet": profile["known_gaps"][0], "subreddit": "Analyst Note"}]
            
        if reddit_quotes:
            for quote in reddit_quotes[:3]:
                if isinstance(quote, dict):
                    title = quote.get("title", "")
                    snippet = quote.get("snippet", "")
                    sub = quote.get("subreddit", "")
                    display_text = f"<b>{title}</b><br>{snippet}<br><i>- {sub}</i>"
                else:
                    display_text = quote
                st.markdown(f"""
                <div style='border-left: 2px solid #FF4500; background: #161B22; padding: 12px; margin-bottom: 8px; border-radius: 4px; color: #EEEDEB; font-size: 13px;'>
                    {display_text}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No localized public signals found right now.")

        st.divider()

        # SECTION 7: AI Pre-meeting Memo
        st.markdown("#### Executive Briefing")
        if st.button("Generate CPO Pre-meeting Brief", key=f"cpo_brief_{company_name}"):
            with st.spinner("Analyzing profile & live signals..."):
                try:
                    groq_api_key = st.secrets.get("GROQ_API_KEY", "")
                    if not groq_api_key or "gsk_" not in groq_api_key:
                        st.error("Valid GROQ_API_KEY is missing from .streamlit/secrets.toml")
                    else:
                        client = Groq(api_key=groq_api_key)
                        
                        sys_prompt = "You are a senior strategy consultant preparing a client for a C-suite meeting. Be specific, direct, and actionable. Max 200 words total."
                        user_prompt = f"""
Company: {company_name} in {sector_name}
Valuation: ${profile.get('valuation_usd_bn', 'Undisclosed')}Bn
ICP: {profile.get('icp', 'N/A')}
Known gaps: {', '.join(profile.get('known_gaps', [])[:2])}
Current hiring: {open_roles} open roles

Write a 3-bullet pre-meeting brief:
1. The one thing this company is most proud of right now
2. The one thing they are most anxious about (based on their gaps)
3. The angle you should open with to make them feel understood
"""
                        resp = client.chat.completions.create(
                            model="llama3-70b-8192",
                            messages=[
                                {"role": "system", "content": sys_prompt},
                                {"role": "user", "content": user_prompt}
                            ],
                            max_tokens=300
                        )
                        st.session_state[f"memo_{company_name}"] = resp.choices[0].message.content
                except Exception as e:
                    st.error(f"Failed to generate brief via Groq: {e}")

        if f"memo_{company_name}" in st.session_state:
            st.markdown(f"""
            <div style='background: #1A1525; border: 1px solid #B388FF; padding: 16px; border-radius: 8px; color: #EEEDEB; font-size: 14px; line-height: 1.6;'>
                {st.session_state[f"memo_{company_name}"].replace(chr(10), "<br>")}
            </div>
            """, unsafe_allow_html=True)
