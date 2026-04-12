import streamlit as st
import plotly.graph_objects as go

COLORS = {"A": "#378ADD", "B": "#D85A30"}

def render_comparison(
    company_a: str, company_b: str,
    ratings: dict, jobs: dict, news: dict, glassdoor: dict,
    trends_df,
):
    st.markdown("### Head-to-Head Comparison")
    st.caption(f"{company_a} vs {company_b}")
    
    # Header strip
    col_a, col_mid, col_b = st.columns([5, 1, 5])
    with col_a:
        st.markdown(f"""
        <div style="background: #161B22; border: 1px solid #378ADD; border-radius: 12px; padding: 20px; text-align: center;">
          <div style="font-size: 2.5rem; font-weight: 800; color: #378ADD; margin-bottom: 4px;">{company_a[0]}</div>
          <div style="font-size: 1.2rem; font-weight: 700; color: #FFFFFF;">{company_a}</div>
          <div style="font-size: 0.75rem; color: #8B949E; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.1em;">Company A</div>
        </div>
""", unsafe_allow_html=True)
    with col_mid:
        st.markdown("<div style='display:flex; align-items:center; justify-content:center; height:100%; font-weight:800; color:#8B949E; font-size:1.2rem;'>vs</div>", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div style="background: #161B22; border: 1px solid #D85A30; border-radius: 12px; padding: 20px; text-align: center;">
          <div style="font-size: 2.5rem; font-weight: 800; color: #D85A30; margin-bottom: 4px;">{company_b[0]}</div>
          <div style="font-size: 1.2rem; font-weight: 700; color: #FFFFFF;">{company_b}</div>
          <div style="font-size: 0.75rem; color: #8B949E; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.1em;">Company B</div>
        </div>
""", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)
    
    # Metrics comparison
    metrics = [
        ("App Rating", 
         ratings.get(company_a,{}).get("rating",0),
         ratings.get(company_b,{}).get("rating",0), 5.0),
        ("Open Roles",
         jobs.get(company_a,0), jobs.get(company_b,0),
         max(jobs.get(company_a,1), jobs.get(company_b,1)) * 1.2),
        ("News Mentions",
         news.get(company_a,0), news.get(company_b,0),
         max(news.get(company_a,1), news.get(company_b,1)) * 1.2),
        ("Employer Score",
         glassdoor.get(company_a,0), glassdoor.get(company_b,0), 5.0),
    ]
    
    for label, val_a, val_b, max_val in metrics:
        pct_a = min(int((val_a / max_val) * 100), 100) if max_val else 0
        pct_b = min(int((val_b / max_val) * 100), 100) if max_val else 0
        winner = "A" if val_a > val_b else ("B" if val_b > val_a else "tie")
        
        st.markdown(f"""
        <div style="margin-bottom: 24px;">
          <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <div style="font-family: 'Manrope'; font-weight: 700; color: {'#378ADD' if winner=='A' else '#8B949E'};">{val_a if isinstance(val_a,int) else f"{val_a:.1f}"}</div>
            <div style="font-size: 0.85rem; color: #EEEDEB; font-weight: 600;">{label}</div>
            <div style="font-family: 'Manrope'; font-weight: 700; color: {'#D85A30' if winner=='B' else '#8B949E'};">{val_b if isinstance(val_b,int) else f"{val_b:.1f}"}</div>
          </div>
          <div style="display: flex; height: 10px; background: #21262D; border-radius: 5px; overflow: hidden;">
              <div style="width: 50%; display: flex; justify-content: flex-end;">
                <div style="width: {pct_a}%; height: 100%; background: #378ADD; border-radius: 5px 0 0 5px;"></div>
              </div>
              <div style="width: 2px; background: #30363D;"></div>
              <div style="width: 50%;">
                <div style="width: {pct_b}%; height: 100%; background: #D85A30; border-radius: 0 5px 5px 0;"></div>
              </div>
          </div>
        </div>
""", unsafe_allow_html=True)
    
    # Trend overlay
    if not trends_df.empty:
        cp_a = company_a if company_a in trends_df.columns else None
        cp_b = company_b if company_b in trends_df.columns else None
        if cp_a or cp_b:
            fig = go.Figure()
            df_r = trends_df.reset_index()
            date_col = df_r.columns[0]
            if cp_a:
                fig.add_trace(go.Scatter(x=df_r[date_col], y=trends_df[cp_a],
                    name=company_a, line=dict(color="#378ADD", width=2.5)))
            if cp_b:
                fig.add_trace(go.Scatter(x=df_r[date_col], y=trends_df[cp_b],
                    name=company_b, line=dict(color="#D85A30", width=2.5)))
            fig.update_layout(
                paper_bgcolor="#161B22", plot_bgcolor="#0D1117",
                height=200, margin=dict(l=10,r=10,t=10,b=10),
                legend=dict(orientation="h", y=-0.3, bgcolor="#161B22",
                            font=dict(color="#8B949E",size=10)),
                yaxis=dict(gridcolor="#21262D", showticklabels=False),
                xaxis=dict(gridcolor="rgba(0,0,0,0)", showticklabels=False),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
