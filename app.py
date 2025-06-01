import streamlit as st
import pdfplumber
from sentence_transformers import SentenceTransformer, util

st.title("Free AI Resume Matcher")

resume_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste the Job Description here")

# Load sentence transformer model (first time may take a few minutes)
model = SentenceTransformer('all-MiniLM-L6-v2')

if st.button("Analyze Resume"):
    if resume_file and job_description:
        # Extract resume text
        with pdfplumber.open(resume_file) as pdf:
            resume_text = ""
            for page in pdf.pages:
                resume_text += page.extract_text()

        # Create embeddings
        resume_embed = model.encode(resume_text, convert_to_tensor=True)
        job_embed = model.encode(job_description, convert_to_tensor=True)

        # Compare
        score = util.pytorch_cos_sim(resume_embed, job_embed).item() * 100

        st.subheader("Match Score:")
        st.write(f"{score:.2f} %")

        st.subheader("Suggestions:")
        st.write("Try to include more keywords from the job description in your resume. Use bullet points to highlight relevant skills.")
    else:
        st.warning("Please upload a resume and paste the job description.")
