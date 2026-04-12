import streamlit as st

def render_founder_panel(company_name: str, profile: dict):
    leadership = profile.get("leadership", [])
    if not leadership:
        return
    
    st.markdown("#### Leadership Intelligence")
    
    cols = st.columns(min(len(leadership), 3))
    for i, person in enumerate(leadership[:3]):
        with cols[i]:
            initials = "".join([w[0] for w in person["name"].split()[:2]]).upper()
            avatar_color = ["#378ADD", "#1D9E75", "#D85A30"][i % 3]
            
            st.markdown(f"""
            <div style="background: #161B22; border: 1px solid #21262D; border-radius: 12px; padding: 16px; margin-bottom: 20px; transition: transform 0.2s ease;">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                    <div style="width: 42px; height: 42px; border-radius: 50%; background: {avatar_color}; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 0.9rem;">
                        {initials}
                    </div>
                    <div>
                        <div style="font-family: 'Manrope', sans-serif; font-weight: 700; font-size: 0.95rem; color: #FFFFFF;">
                            {person['name']}
                        </div>
                        <div style="font-family: 'Inter', sans-serif; font-size: 0.75rem; color: #8B949E;">
                            {person['role']}
                        </div>
                    </div>
                </div>
                <div style="border-top: 1px solid #21262D; padding-top: 12px;">
                    <p style="font-size: 0.8rem; color: #E6EDF3; margin-bottom: 8px;">
                        <span style="color: #8B949E; font-weight: 500;">Background:</span> {person.get('background') or 'Background undisclosed'}
                    </p>
                    <p style="font-size: 0.8rem; color: #E6EDF3; margin-bottom: 8px;">
                        <span style="color: #8B949E; font-weight: 500;">Known For:</span> {person.get('known_for') or 'N/A'}
                    </p>
                    { f"<p style='font-size: 0.75rem; color: #B388FF; background: rgba(179, 136, 255, 0.1); padding: 8px; border-radius: 4px; border-left: 2px solid #B388FF; margin-top: 10px;'><b>Signal:</b> {person['competitive_signal']}</p>" if person.get('competitive_signal') else "" }
                    { f"<p style='font-size: 0.7rem; color: #8B949E; margin-top: 10px;'><b>Hiring from:</b> {', '.join(person['hire_from'])}</p>" if person.get('hire_from') else "" }
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if person.get("linkedin_url"):
                st.caption(f"[LinkedIn Profile]({person['linkedin_url']})")
