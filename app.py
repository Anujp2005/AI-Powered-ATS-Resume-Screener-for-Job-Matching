from dotenv import load_dotenv

load_dotenv()

import base64
import streamlit as st 
import os 
import io
import fitz
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text
    
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in pdf_doc:
            text += page.get_text("text")
        return text
    else:
        raise FileNotFoundError("No file uploaded")
    
## Streamlit App 

st.set_page_config(page_title="ATS Resume Screener", layout="wide")

# Header 

st.markdown("<h1 style='text-align: center; color:#2E86C1;'>📋 ATS Resume Screener</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color:gray;'>Upload your resume, compare with job descriptions, and get ATS-style AI insights instantly.</p>", unsafe_allow_html=True)
st.markdown("---")

# Layout

col1, col2 = st.columns([2, 1])

with col1:
    job_description = st.text_area("📝 Paste the Job Description Here", height=200, key="input")

with col2:
    uploaded_file = st.file_uploader("📂 Upload Resume (PDF Only)",type=["pdf"])
    if uploaded_file is not None:
        st.success("✅ Resume uploaded successfully!")

st.markdown("---")

# Tabs for Evaluation Options

tab1, tab2 = st.tabs(["📄 Resume Evaluation", "📊 ATS Match Score"])

# Prompts

input_prompt1 = """
You are an experienced HR professional with technical knowledge in Data Science, 
Fullstack Development, Web Development, Big Data Engineering, DevOps, and Data Analysis.  

Your task is to review the candidate's resume against the provided job description.  

Please provide a professional evaluation that includes:
1. Whether the candidate’s profile aligns with the job requirements.
2. The strengths of the candidate relevant to the role.
3. The weaknesses or gaps in relation to the specified job.
4. A final recommendation on suitability for shortlisting.
"""

input_prompt3 = """
You are an advanced Applicant Tracking System (ATS) scanner with deep knowledge of 
Data Science, Web Development, Big Data Engineering, DevOps, and Data Analysis roles.  

Your task is to evaluate the candidate's resume against the provided job description.  

Please provide the output in the following format:
1. A match percentage (0–100%) showing how well the resume aligns with the job description.
2. A list of important keywords/skills from the job description that are present in the resume.
3. A list of missing keywords/skills that the candidate should add to improve their ATS score.
4. A short summary of the candidate’s overall suitability for the role.
"""

# Tab1 - Resume Evaluation

with tab1:
    st.markdown("### 📄 Detailed HR-style Resume Review")
    if st.button("🔎 Run Resume Evaluation", key="btn1"):
        if uploaded_file is not None and job_description.strip() != "":
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt1, pdf_content, job_description)
            st.success("✅ Evaluation Completed")
            st.markdown("#### 🔍 AI Evaluation Result")
            st.write(response)
        else:
            st.warning("⚠️ Please upload a resume and enter job description.")

# Tab2 - ATS Match Score

with tab2:
    st.markdown("### 📊 ATS Matching & Keyword Analysis")
    if st.button("📈 Run ATS Scoring", key="btn3"):
        if uploaded_file is not None and job_description.strip() != "":
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt3, pdf_content, job_description)
            st.success("✅ ATS Scoring Completed")
            st.markdown("#### 📈 ATS Report")
            st.write(response)
        else:
            st.warning("⚠️ Please upload a resume and enter job description.")
        
