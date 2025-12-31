import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="AI Resume Helper", page_icon="📄")
st.title("📄 AI Resume Helper")

# 🔐 Load API key safely
api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ Google API key not found")
    st.stop()

# ✅ Configure Gemini
genai.configure(api_key=api_key)

# ✅ AUTO-FIND a working text model (THIS IS THE FIX)
model = None
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        model = genai.GenerativeModel(m.name)
        st.success(f"✅ Using model: {m.name}")
        break

if model is None:
    st.error("❌ No text generation model available for this API key.")
    st.stop()

# ---------------- UI ----------------
resume_text = st.text_area("Paste your resume here", height=250)
job_role = st.text_input("Target Job Role")

if st.button("✨ Improve Resume"):
    if not resume_text or not job_role:
        st.warning("Please fill both fields.")
    else:
        prompt = f"""
You are an expert resume reviewer.

Improve the resume below for the role of {job_role}.
Provide:
- Strong bullet points
- Action verbs
- Missing technical & soft skills
- ATS-friendly suggestions

Resume:
{resume_text}
"""
        with st.spinner("Improving your resume..."):
            response = model.generate_content(prompt)

        st.subheader("✅ Improved Resume")
        st.write(response.text)
