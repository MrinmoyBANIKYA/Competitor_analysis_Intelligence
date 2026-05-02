import streamlit as st
from groq import Groq
import json

def get_groq_client():
    """Reads GROQ_API_KEY from st.secrets and returns a Groq client."""
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
        if not api_key:
            return None
        return Groq(api_key=api_key)
    except Exception:
        return None

def generate_sector_analysis(sector_name, sector_data_dict):
    """
    Builds a structured prompt with the sector data and calls Groq for analysis.
    Returns a dict with analysis components or an error.
    """
    client = get_groq_client()
    if not client:
        return {"error": "API key not configured"}
    
    # Sanitize sector data for prompt
    context_data = {
        "sector": sector_name,
        "metrics": sector_data_dict.get("metrics", {}),
        "companies": sector_data_dict.get("companies", []),
        "news_mentions": sector_data_dict.get("news", {}),
        "hiring_trends": sector_data_dict.get("jobs", {}),
        "app_ratings": sector_data_dict.get("ratings", {})
    }

    prompt = f"""
    You are an elite strategy analyst for NixTio, specialized in the Indian startup ecosystem.
    Analyze the {sector_name} sector based on this real-time intelligence data:
    
    {json.dumps(context_data, indent=2)}
    
    Provide a high-impact, executive-level analysis. 
    You MUST return the response as a JSON object with exactly these keys:
    - momentum: Analysis of sector speed, growth trajectory and current 'vibe'.
    - competitive_position: Identification of the market leader, the fastest challenger, and the 'why' behind their positions.
    - talent_signal: Deep dive into what the hiring data (LinkedIn jobs) suggests about their product roadmap (e.g., expansion into new cities, new tech stack, etc).
    - risk_factors: Clear-eyed assessment of regulatory, competitive, or operational risks.
    - recommendations: Three specific, actionable "So what?" moves for an operator or investor.

    Style: Sharp, data-driven, zero fluff. No generic advice.
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a professional sector analyst that only outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

def stream_analyst_response(question, context):
    """Streams a response from the analyst for follow-up chat."""
    client = get_groq_client()
    if not client:
        yield "Error: Groq API key is not configured in settings."
        return
    
    system_msg = "You are a sharp NixTio strategy analyst. Answer questions based on the provided sector context. Be direct, specific, and data-backed. Max 150 words."
    user_msg = f"Context: {context}\n\nQuestion: {question}"
    
    try:
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.3,
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        yield f"Error during streaming: {str(e)}"
