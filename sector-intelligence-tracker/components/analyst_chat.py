from groq import Groq
import streamlit as st

def render_analyst_sidebar(sector_name, companies, live_data, sector_meta):
    """Renders the personalized CXO analyst panel in the sidebar."""
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Your Analyst**")
    
    # User context — stored in session_state
    if "user_role" not in st.session_state:
        st.session_state["user_role"] = ""
    if "user_company" not in st.session_state:
        st.session_state["user_company"] = ""
    
    role = st.sidebar.text_input(
        "Your role", 
        value=st.session_state["user_role"],
        placeholder="e.g. CPO at Zepto",
        key="role_input"
    )
    company = st.sidebar.text_input(
        "Your company",
        value=st.session_state["user_company"], 
        placeholder="e.g. Zepto",
        key="company_input"
    )
    st.session_state["user_role"] = role
    st.session_state["user_company"] = company
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Ask your analyst**")
    
    question = st.sidebar.text_area(
        "Question",
        placeholder="e.g. Which company here is most likely to eat into our market share in the next 6 months?",
        height=100,
        label_visibility="collapsed",
        key="analyst_q"
    )
    
    if st.sidebar.button("Ask", type="primary", use_container_width=True):
        if not question.strip():
            st.sidebar.warning("Type a question first.")
            return
        
        # Build rich context from all live data
        ratings_summary = {c: live_data["ratings"].get(c,{}).get("rating",0) for c in companies}
        jobs_summary = {c: live_data["jobs"].get(c,0) for c in companies}
        news_summary = {c: live_data["news"].get(c,0) for c in companies}
        glassdoor_summary = {c: live_data["glassdoor"].get(c,3.5) for c in companies}
        
        system_prompt = f"""You are an elite strategy analyst at a top-tier firm, acting as the personal analyst for {role or 'a senior executive'} at {company or 'their company'}.

You have access to real-time competitive intelligence on the {sector_name} sector in India.

Your style:
- Sharp, direct, no filler words
- Specific company names and numbers, not vague generalities  
- Always end with one clear "So what?" recommendation
- Max 150 words total
- Never say "I think" or "perhaps" — speak with the confidence of someone who has analyzed this sector for years"""

        user_prompt = f"""Sector: {sector_name}
Market size: ${sector_meta.get('tam_usd_bn','N/A')}Bn TAM, {sector_meta.get('cagr_pct','N/A')}% CAGR
Companies: {', '.join(companies)}
App ratings: {ratings_summary}
Open roles (hiring): {jobs_summary}
News mentions (30d): {news_summary}
Employer scores: {glassdoor_summary}
Unsolved problems: {sector_meta.get('unsolved_problems', [])}

{f"User context: I am {role} at {company}." if role and company else ""}

Question: {question}"""

        with st.sidebar.spinner("Thinking..."):
            try:
                groq_api_key = st.secrets.get("GROQ_API_KEY", "")
                if not groq_api_key or "gsk_" not in groq_api_key:
                    st.sidebar.error("Valid GROQ_API_KEY is missing from .streamlit/secrets.toml")
                    return
                client = Groq(api_key=groq_api_key)
                msg = client.chat.completions.create(
                    model="llama3-70b-8192",
                    max_tokens=400,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                answer = msg.choices[0].message.content
                
                # Store in chat history
                if "analyst_history" not in st.session_state:
                    st.session_state["analyst_history"] = []
                st.session_state["analyst_history"].append({"q": question, "a": answer})
                
            except Exception as e:
                st.sidebar.error(f"API error: {e}")
                return
    
    # Show chat history (most recent first)
    history = st.session_state.get("analyst_history", [])
    for item in reversed(history[-5:]):
        st.sidebar.markdown(f"**Q:** {item['q'][:60]}...")
        st.sidebar.markdown(f"""
        <div style='background-color:#1A1525; padding:12px; border-radius:8px; font-size:13px; color:#EEEDEB; border-left:3px solid #B388FF'>
        {item['a']}
        </div>
        """, unsafe_allow_html=True)
