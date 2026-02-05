import sqlite3
import pandas as pd
import os

# =====================================================
# Paths
# =====================================================
CSV_PATH = "data/processed/faculty_clean.csv"
DB_PATH = "database/faculty.db"

os.makedirs("database", exist_ok=True)

# =====================================================
# Load cleaned faculty CSV
# =====================================================
df = pd.read_csv(CSV_PATH).fillna("")

# =====================================================
# Build rich semantic context
# =====================================================
def build_semantic_text(row):
    return f"""
    Faculty Name: {row['name']}
    Specialization: {row['specialization']}
    Teaching Areas: {row['teaching']}
    Biography: {row['bio']}
    """

df["semantic_text"] = df.apply(build_semantic_text, axis=1)

# =====================================================
# Store in SQLite
# =====================================================
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS faculty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    specialization TEXT,
    teaching TEXT,
    bio TEXT,
    phone TEXT,
    email TEXT,
    profile_url TEXT UNIQUE,
    semantic_text TEXT
)
""")

for _, row in df.iterrows():
    cursor.execute("""
        INSERT OR IGNORE INTO faculty
        (name, specialization, teaching, bio, phone, email, profile_url, semantic_text)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row["name"],
        row["specialization"],
        row["teaching"],
        row["bio"],
        row["phone"],
        row["email"],
        row["profile_url"],
        row["semantic_text"]
    ))

conn.commit()
conn.close()

print("✅ Faculty stored with semantic context (faculty.db)")
