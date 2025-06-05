import streamlit as st
import pdfplumber
from sentence_transformers import SentenceTransformer, util
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

from db_setup import save_analysis_resume  # Only this is needed

st.set_page_config(page_title="AI Resume Matcher", layout="centered")
st.title("🎯 Free AI Resume Matcher")

# Load AI model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# --- Utility to extract meaningful keywords ---
def extract_keywords(text):
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    stop_words = set(stopwords.words('english'))
    custom_stops = {
        "candidates", "hiring", "know", "plus", "reporting",
        "stakeholder", "working", "should", "must", "will",
        "requirement", "preferred", "communication", "looking",
        "apply", "responsibilities", "knowledge", "skilled"
    }
    return set([w for w in words if w not in stop_words and w not in custom_stops])

# --- Input Fields ---
username = st.text_input("Enter your name:")
resume_file = st.file_uploader("Upload a Resume to Analyze (PDF)", type=["pdf"])
job_description = st.text_area("Paste the Job Description here")

# --- Analyze Button ---
if st.button("🔍 Analyze Resume"):
    if username and resume_file and job_description:
        with pdfplumber.open(resume_file) as pdf:
            resume_text = "".join([page.extract_text() or "" for page in pdf.pages])

        # Vector encoding
        resume_embed = model.encode(resume_text, convert_to_tensor=True)
        job_embed = model.encode(job_description, convert_to_tensor=True)

        # Similarity Score
        score = util.pytorch_cos_sim(resume_embed, job_embed).item() * 100
        st.subheader("✅ Match Score:")
        st.write(f"{score:.2f} %")

        # Save analysis only (no profile info here)
        save_analysis_resume(username.strip(), resume_text, job_description, f"{score:.2f}")
        st.success("📊 Analysis saved to your history.")

        # Keyword suggestions
        resume_keywords = extract_keywords(resume_text)
        job_keywords = extract_keywords(job_description)
        missing_keywords = sorted(list(job_keywords - resume_keywords))

        st.subheader("🧠 Keyword Suggestions:")
        if missing_keywords:
            st.write("Try including these keywords in your resume:")
            st.write(", ".join(missing_keywords[:15]))
        else:
            st.write("🎉 Your resume already covers most of the job description!")
    else:
        st.warning("Please enter your name, upload a resume, and paste the job description.")
