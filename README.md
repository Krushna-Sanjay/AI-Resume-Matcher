# 📄 AI Resume Matcher

An AI-powered Streamlit web app that analyzes and matches resumes with job descriptions using Google's Generative AI (Gemini). It also allows users to manage their profile, upload resumes, and track past analyses — all stored in a local SQLite database.

🔗 [Live App](https://ai-resume-matcher-ltgbc5vwuxfk72mcxihwpb.streamlit.app/)

---

## 💡 Features

🧠 **LLM-Powered Resume Analysis**  
Leverages Google’s Gemini (a state-of-the-art large language model) to understand and evaluate resumes against job descriptions with high accuracy.

📄 **Advanced PDF Parsing**  
Uses `pdfplumber` to extract clean, structured resume text from uploaded PDF files.

🧑‍💼 **User Profile Management**  
Create, update, and manage user profiles with email and resume, stored securely in a local SQLite database.

📊 **Resume Match History**  
Tracks and displays previous analyses for each user, including timestamps and relevance scores.

📥 **Downloadable Resume Content**  
Allows users to export parsed resume text into a downloadable TXT format.

🎨 **Simple & Responsive UI**  
Built with Streamlit for a clean and interactive experience across devices, with immediate feedback and minimal distraction.

☁️ **Streamlit Cloud Ready**  
Easily deployable to [Streamlit Cloud](https://streamlit.io/cloud) with no additional infrastructure setup.

---

## 🛠 Tech Stack

| Layer         | Tools/Technologies                          |
|---------------|---------------------------------------------|
| Frontend      | Streamlit                                   |
| Backend       | Python, Google Generative AI (Gemini - LLM) |
| PDF Parsing   | pdfplumber                                  |
| Database      | SQLite (via `sqlite3` module)               |
| Deployment    | Streamlit Cloud                             |

---

## 🗃️ Project Structure

```bash
ai-resume-matcher/
├── .streamlit/
│   └── secrets.toml         # API key (not pushed to Git)
├── db_setup.py              # Handles DB setup and functions
├── Analyzer.py              # Main resume matcher logic
├── pages/
│   └── User_Profile.py      # User profile management
├── resume_matcher.db        # SQLite database (auto-created)
├── requirements.txt         # Python dependencies
└── README.md                # Project description
```

---

## 🚀 Getting Started (Local Setup)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/ai-resume-matcher.git
   cd ai-resume-matcher
   ```

2. **Create a virtual environment and activate it (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Add your Gemini API Key:**

   Create a file at `.streamlit/secrets.toml` and paste:

   ```toml
   GEMINI_API_KEY = "your_gemini_api_key"
   ```

5. **Run the app:**

   ```bash
   streamlit run Analyzer.py
   ```

---

## ☁️ Deploy on Streamlit Cloud

1. Push your project to GitHub.

2. Visit [streamlit.io/cloud](https://streamlit.io/cloud) and log in.

3. Click **"New App"** and select your GitHub repository.

4. Set `Analyzer.py` as the **main file**.

5. Add your Gemini API key in the **Secrets** section:

   ```toml
   GEMINI_API_KEY = "your_gemini_api_key"
   ```

6. Click **"Deploy"**. Your app will be live in seconds 🚀

---

## 🧪 Example Use Cases

* Job seekers checking how well their resume fits a specific job.
* Recruiters evaluating applicant fit based on job requirements.
* Students and developers showcasing real-world GenAI/NLP skills in a portfolio project.

---

## 🛡️ Notes

* Ensure `.streamlit/secrets.toml` is **not pushed to GitHub**. Add it to `.gitignore`.
* Database (`resume_matcher.db`) is generated automatically.
* You can delete the local database file to reset all user data and analysis history.

---

## 📬 Contact

For feedback or contributions, feel free to open an issue or fork the repo.
Made with ❤️ using Python and Streamlit.



