import os
import sqlite3
import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# =====================================================
# Database configuration
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "faculty.db")


# =====================================================
# Load faculty data from SQLite
# =====================================================
def load_faculty_data():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        """
        SELECT id, name, bio_text, profile_url
        FROM faculty
        """,
        conn
    )

    conn.close()

    # Ensure clean text for embeddings
    df["bio_text"] = df["bio_text"].fillna("").astype(str)

    return df


# =====================================================
# Load sentence embedding model
# =====================================================
model = SentenceTransformer("all-MiniLM-L6-v2")


# =====================================================
# Generate embeddings
# =====================================================
def generate_embeddings(texts):
    return model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True
    )


# =====================================================
# Semantic recommendation logic
# =====================================================
def recommend_faculty(query, df, embeddings, top_k=5):
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    similarities = cosine_similarity(query_embedding, embeddings)[0]

    df = df.copy()
    df["similarity_score"] = similarities

    results = (
        df.sort_values("similarity_score", ascending=False)
        .head(top_k)
        .reset_index(drop=True)
    )

    return results[["id", "name", "profile_url", "similarity_score"]]


# =====================================================
# Local testing (Data Scientist verification)
# =====================================================
if __name__ == "__main__":
    print("Loading faculty data...")
    faculty_df = load_faculty_data()

    print("Generating embeddings...")
    faculty_embeddings = generate_embeddings(
        faculty_df["bio_text"].tolist()
    )

    test_query = "sustainable energy and carbon capture"

    print(f"\nQuery: {test_query}\n")
    recommendations = recommend_faculty(
        test_query,
        faculty_df,
        faculty_embeddings
    )

    print(recommendations)
