import sqlite3
import pandas as pd
import os

CSV_PATH = "data/processed/faculty_clean.csv"
DB_PATH = "database/faculty.db"

os.makedirs("database", exist_ok=True)

df = pd.read_csv(CSV_PATH)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS faculty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    bio TEXT,
    specialization TEXT,
    teaching TEXT,
    phone TEXT,
    email TEXT,
    profile_url TEXT UNIQUE,
    bio_text TEXT
)
""")

for _, row in df.iterrows():
    cursor.execute("""
    INSERT OR IGNORE INTO faculty
    (name, bio, specialization, teaching, phone, email, profile_url, bio_text)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row["name"],
        row["bio"],
        row["specialization"],
        row["teaching"],
        row["phone"],
        row["email"],
        row["profile_url"],
        row["bio_text"]
    ))

conn.commit()
conn.close()

print("  Storage complete: faculty.db created")
