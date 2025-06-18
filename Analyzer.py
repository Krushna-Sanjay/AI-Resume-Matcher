import streamlit as st
import pdfplumber
import google.generativeai as genai
from db_setup import save_analysis_resume

# Set your Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Load the Gemini model (choose a valid one)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")  # You can switch to a different valid one

# Streamlit page setup
st.set_page_config(page_title="AI Resume Matcher", layout="centered")
st.title("📄 AI Resume Matcher")

# Input Fields
username = st.text_input("Enter your name:")
resume_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste the Job Description here")

# Function to calculate match score
def get_match_score(resume_text, job_description):
    prompt = f"""
    You are a resume screening expert.

    Compare the following resume with the job description and provide a match score (from 0 to 100) indicating how well the resume fits the job.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Respond ONLY with the match score as a percentage number (e.g., "76").
    """
    response = model.generate_content(prompt)
    return response.text.strip()

# Function to get suggestions
def get_improvement_suggestions(resume_text, job_description):
    prompt = f"""
    You are a helpful resume coach.

    A candidate uploaded their resume and a job description. Suggest improvements to align the resume better with the job.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Provide clear, actionable suggestions in bullet points.
    """
    response = model.generate_content(prompt)
    return response.text.strip()

# Main button logic
if st.button("Analyze Resume"):
    if username and resume_file and job_description:
        try:
            with pdfplumber.open(resume_file) as pdf:
                resume_text = "".join([page.extract_text() or "" for page in pdf.pages])

            with st.spinner("Calculating match score..."):
                score_text = get_match_score(resume_text, job_description)
                match_score = int(''.join(filter(str.isdigit, score_text)))

            # Display score
            st.subheader(f"✅ Match Score for {username}:")
            st.metric(label="Match Score (%)", value=f"{match_score}%")
            st.progress(match_score)

            save_analysis_resume(username, resume_text, job_description, match_score)

            # Color badge
            color = "green" if match_score >= 75 else "orange" if match_score >= 50 else "red"
            st.markdown(f"""
                <div style="background-color:{color};padding:10px;border-radius:5px;color:white;text-align:center;">
                    Match Score: {match_score}%
                </div>
            """, unsafe_allow_html=True)

            # Suggestions
            with st.spinner("Generating improvement suggestions..."):
                suggestions = get_improvement_suggestions(resume_text, job_description)

            st.subheader("📌 Suggestions to Improve Your Resume:")
            st.markdown(suggestions)

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
    else:
        st.warning("Please fill in all fields (name, resume, job description).")

