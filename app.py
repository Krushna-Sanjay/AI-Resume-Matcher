import streamlit as st
import pdfplumber
from sentence_transformers import SentenceTransformer, util
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

from db_setup import save_or_update_main_resume, save_analysis_resume

st.set_page_config(page_title="AI Resume Matcher", layout="centered")
st.title("Free AI Resume Matcher")

# Load AI model
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_keywords(text):
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    stop_words = set(stopwords.words('english'))
    custom_stops = {"candidates", "hiring", "know", "plus", "reporting",
                    "stakeholder", "working", "should", "must", "will",
                    "requirement", "preferred", "communication", "looking", "apply", "responsibilities", "knowledge", "skilled"}
    return set([w for w in words if w not in stop_words and w not in custom_stops])

username = st.text_input("Enter your name:")
email = st.text_input("Enter your email (optional):")
resume_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste the Job Description here")

if st.button("Analyze Resume"):
    if username and resume_file and job_description:
        with pdfplumber.open(resume_file) as pdf:
            resume_text = "".join([page.extract_text() or "" for page in pdf.pages])

        resume_embed = model.encode(resume_text, convert_to_tensor=True)
        job_embed = model.encode(job_description, convert_to_tensor=True)

        score = util.pytorch_cos_sim(resume_embed, job_embed).item() * 100
        st.subheader("Match Score:")
        st.write(f"{score:.2f} %")

        save_or_update_main_resume(username.strip(), email.strip(), resume_text)
        save_analysis_resume(username.strip(), resume_text, job_description, score)
        st.success("✅ Saved your profile resume & this analysis!")

        resume_keywords = extract_keywords(resume_text)
        job_keywords = extract_keywords(job_description)
        missing_keywords = sorted(list(job_keywords - resume_keywords))

        st.subheader("Suggestions:")
        if missing_keywords:
            st.write("Try including these keywords in your resume:")
            st.write(", ".join(missing_keywords[:15]))
        else:
            st.write("Awesome! Your resume already covers most of the job description.")
    else:
        st.warning("Please enter your name, upload a resume, and paste the job description.")
