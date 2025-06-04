import streamlit as st
import pdfplumber
from db_setup import save_or_update_main_resume, get_user_profile

st.set_page_config(page_title="User Profile", layout="centered")
st.title("User Profile")

# Input form to update profile
profile_name = st.text_input("Enter your username to view/edit profile:")
email_update = st.text_input("Update Email (optional):")
resume_file = st.file_uploader("Upload your main profile resume (PDF)", type=["pdf"])  # Unique key not needed here

if st.button("Save / Update Profile"):
    if profile_name and resume_file:
        with pdfplumber.open(resume_file) as pdf:
            resume_text = "".join([page.extract_text() or "" for page in pdf.pages])
        save_or_update_main_resume(profile_name.strip(), email_update.strip(), resume_text)
        st.success("✅ Profile updated and resume saved.")
    else:
        st.warning("Please enter your name and upload a resume.")

# Show profile info
if profile_name:
    profile = get_user_profile(profile_name.strip())
    if profile:
        st.subheader("User Profile")
        st.write(f"**Name:** {profile['username']}")
        st.write(f"**Email:** {profile['email'] or 'Not provided'}")
        st.write(f"**Created At:** {profile['created_at']}")

        st.subheader("Main Resume")
        st.text_area("Main Resume Text", profile['main_resume'], height=300)
    else:
        st.error("User profile not found.")
