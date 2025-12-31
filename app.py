import streamlit as st
import google.generativeai as genai

# 🔑 API KEY (temporary – OK for prototype)
api_key = "AIzaSyB1wkiYky_OSqrKuAfG0NBMc8QurTPXtng"

client = genai.Client(api_key=api_key)

st.set_page_config(page_title="AI Resume Helper", page_icon="📄")
st.title("📄 AI Resume Helper")

# 🔍 Find a supported text model
models = client.models.list()
text_model = None

for m in models:
    if "generateContent" in m.supported_actions:
        text_model = m.name
        break

if not text_model:
    st.error("❌ No text generation model available for this API key.")
    st.stop()

st.success(f"✅ Using model: {text_model}")

resume_text = st.text_area("Paste your resume here", height=250)
job_role = st.text_input("Target Job Role")

if st.button("✨ Improve Resume"):
    if resume_text and job_role:
        prompt = f"""
You are an expert resume reviewer.

Improve the resume below for the role of {job_role}.
Provide:
- Stronger bullet points
- Action verbs
- Missing technical & soft skills
- ATS-friendly suggestions

Resume:
{resume_text}
"""

        with st.spinner("Improving your resume..."):
            response = client.models.generate_content(
                model=text_model,
                contents=prompt
            )

        st.subheader("✅ Improved Resume")
        st.write(response.text)
    else:
        st.warning("Please fill both fields.")
