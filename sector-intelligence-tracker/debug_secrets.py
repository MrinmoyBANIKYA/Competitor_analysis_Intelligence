import streamlit as st

st.title("Streamlit Secrets Debugger")

st.write("### st.secrets keys found:")
st.write(list(st.secrets.keys()))

if "GROQ_API_KEY" in st.secrets:
    st.success("GROQ_API_KEY is present!")
    val = st.secrets["GROQ_API_KEY"]
    st.write(f"Key length: {len(val)}")
    st.write(f"Key prefix: {val[:4]}")
else:
    st.error("GROQ_API_KEY is NOT found in st.secrets.")

st.write("---")
st.write("### st.secrets context")
st.write(st.secrets)
