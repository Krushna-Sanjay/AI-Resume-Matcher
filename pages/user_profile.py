import streamlit as st
import pdfplumber
from db_setup import save_analysis_resume, save_or_update_main_resume, get_user_profile, delete_user_profile, get_resume_analysis_history

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


if st.button("Delete Profile"):
    if profile_name:
        profile = get_user_profile(profile_name.strip())  # Check first
        if profile:
            delete_user_profile(profile_name.strip())
            st.success("✅ Your profile has been deleted.")
        else:
            st.error("❌ User profile not found.")
    else:
        st.warning("Please enter a username to delete.")


# Show main profile info
if profile_name:
    profile = get_user_profile(profile_name.strip())
    if profile:
        st.subheader("User Profile")
        st.write(f"**Name:** {profile['username']}")
        st.write(f"**Email:** {profile['email'] or 'Not provided'}")
        st.write(f"**Created At:** {profile['created_at']}")

        st.subheader("Main Resume")
        st.text_area("Main Resume Text", profile['main_resume'], height=300)

        # 📝 Download Resume Button
        st.download_button(
            label="📥 Download Resume",
            data=profile['main_resume'],
            file_name=f"{profile_name}_resume.txt",
            mime="text/plain"
        )
    else:
        st.error("User profile not found.")


st.subheader("📈 Resume Analysis History")
history = get_resume_analysis_history(profile_name.strip())
if history:
    for i, (resume_text, job_desc, score, timestamp) in enumerate(history, 1):
        st.markdown(f"""
            **Analysis #{i}**
            - **Match Score:** {score}%
            - **Analyzed At:** {timestamp}
            - **Resume Snippet:** {resume_text[:150]}...
            - **Job Snippet:** {job_desc[:150]}...
            ---
            """)
    # Export button
    export_data = "\n\n".join([
        f"Match Score: {score}% | Analyzed At: {timestamp}\nResume: {resume_text[:300]}\nJob Description: {job_desc[:300]}"
        for (resume_text, job_desc, score, timestamp) in history
    ])
    st.download_button("📤 Export Full History", data=export_data, file_name=f"{profile_name}_analysis_history.txt", mime="text/plain")
else:
    st.info("No analysis history found.")











