import sqlite3
from datetime import datetime

# DB Connections
conn = sqlite3.connect("resume_matcher.db", check_same_thread=False)
cursor = conn.cursor()

# Tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT,
    main_resume TEXT,
    created_at TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS resume_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    resume_text TEXT,
    job_description TEXT,
    match_score REAL,
    analyzed_at TEXT
)
""")
conn.commit()

# Save or update main resume
def save_or_update_main_resume(username, email, resume_text):
    created_at = datetime.now().isoformat()
    cursor.execute("SELECT * FROM user_profiles WHERE username = ?", (username,))
    if cursor.fetchone():
        cursor.execute("UPDATE user_profiles SET email = ?, main_resume = ? WHERE username = ?", (email, resume_text, username))
    else:
        cursor.execute("INSERT INTO user_profiles (username, email, main_resume, created_at) VALUES (?, ?, ?, ?)",
                       (username, email, resume_text, created_at))
    conn.commit()

# Save analysis
def save_analysis_resume(username, resume_text, job_description, match_score):
    analyzed_at = datetime.now().isoformat()
    cursor.execute("INSERT INTO resume_analysis (username, resume_text, job_description, match_score, analyzed_at) VALUES (?, ?, ?, ?, ?)",
                   (username, resume_text, job_description, match_score, analyzed_at))
    conn.commit()

# Fetch profile
def get_user_profile(username):
    cursor.execute("SELECT username, email, main_resume, created_at FROM user_profiles WHERE username = ?", (username,))
    row = cursor.fetchone()
    if row:
        return {
            "username": row[0],
            "email": row[1],
            "main_resume": row[2],
            "created_at": row[3]
        }
    return None

# Delete profile 
def delete_user_profile(username):
    cursor.execute("DELETE FROM user_profiles WHERE username = ?", (username,))
    # cursor.execute("DELETE FROM resume_analysis WHERE username = ?", (username,))
    conn.commit()


def get_resume_analysis_history(username):
    cursor.execute("SELECT resume_text, job_description, match_score, analyzed_at FROM resume_analysis WHERE username = ?", (username,))
    return cursor.fetchall()


