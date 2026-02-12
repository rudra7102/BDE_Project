from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os

# --------------------
# App initialization
# --------------------
app = FastAPI(
    title="FacultyFinder API",
    docs_url="/docs",
    redoc_url=None
)

# --------------------
# Enable CORS (Production Safe)
# --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # keep * for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# DB Path
# --------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "faculty.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

# --------------------
# Root Redirect
# --------------------
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

# --------------------
# Get All Faculty
# --------------------
@app.get("/all")
def get_all_faculty():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, bio, specialization, teaching, phone, email, profile_url, semantic_text FROM faculty")
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
                "semantic_text": r[8],
            }
            for r in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------------------
# Lazy Load Recommender (IMPORTANT FIX)
# --------------------
faculty_df = None
faculty_embeddings = None

@app.on_event("startup")
def load_embeddings():
    global faculty_df, faculty_embeddings
    from recommender.semantic_search import (
        load_faculty_data,
        generate_embeddings
    )

    faculty_df = load_faculty_data()
    faculty_embeddings = generate_embeddings(
        faculty_df["semantic_text"].tolist()
    )

    print("✅ Faculty embeddings loaded")


# --------------------
# Request Model
# --------------------
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


# --------------------
# Recommend API
# --------------------
@app.post("/recommend")
def recommend(request: QueryRequest):
    try:
        from recommender.semantic_search import recommend_faculty

        results = recommend_faculty(
            request.query,
            faculty_df,
            faculty_embeddings,
            top_k=request.top_k
        )

        return results.to_dict(orient="records")

    except Exception as e:
        print("ERROR IN RECOMMEND:", e)
        raise HTTPException(status_code=500, detail=str(e))


# --------------------
# Local Run
# --------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000)
