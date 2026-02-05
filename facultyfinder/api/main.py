from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel
from typing import Optional

# --------------------
# App initialization
# --------------------
app = FastAPI(title="FacultyFinder API")

DB_PATH = "database/faculty.db"

def get_connection():
    return sqlite3.connect(DB_PATH)


# --------------------
# Existing APIs
# --------------------
@app.get("/all")
def get_all_faculty():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, bio, specialization, teaching,
               phone, email, profile_url, bio_text
        FROM faculty
    """)
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "name": r[1],
            "bio": r[2],
            "specialization": r[3],
            "teaching": r[4],
            "phone": r[5],
            "email": r[6],
            "profile_url": r[7],
            "bio_text": r[8],
        }
        for r in rows
    ]


@app.get("/faculty/{faculty_id}")
def get_faculty_by_id(faculty_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, bio, specialization, teaching,
               phone, email, profile_url, bio_text
        FROM faculty
        WHERE id = ?
    """, (faculty_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": "Faculty not found"}

    return {
        "id": row[0],
        "name": row[1],
        "bio": row[2],
        "specialization": row[3],
        "teaching": row[4],
        "phone": row[5],
        "email": row[6],
        "profile_url": row[7],
        "bio_text": row[8],
    }


# --------------------
# Recommender imports (AFTER app is created)
# --------------------
from recommender.semantic_search import (
    load_faculty_data,
    generate_embeddings,
    recommend_faculty
)


# Load data once
faculty_df = load_faculty_data()
faculty_embeddings = generate_embeddings(
    faculty_df["bio_text"].tolist()
)


# --------------------
# Recommender API
# --------------------
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


@app.post("/recommend")
def recommend(request: QueryRequest):
    results = recommend_faculty(
        request.query,
        faculty_df,
        faculty_embeddings,
        top_k=request.top_k
    )
    return results.to_dict(orient="records")
