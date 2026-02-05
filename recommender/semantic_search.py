import os
import sqlite3
import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# =====================================================
# Paths
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "faculty.db")

# =====================================================
# Load faculty data
# =====================================================
def load_faculty_data():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        """
        SELECT
         id,
         name,
        specialization,
        profile_url,
        name || ' ' || specialization AS semantic_text
        FROM faculty

        """,
        conn
    )

    conn.close()
    df["semantic_text"] = df["semantic_text"].astype(str)
    return df

# =====================================================
# Load embedding model
# =====================================================
model = SentenceTransformer("all-MiniLM-L6-v2")

# =====================================================
# Generate embeddings
# =====================================================
def generate_embeddings(texts):
    return model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

# =====================================================
# Semantic recommendation
# =====================================================
def recommend_faculty(query, faculty_df, faculty_embeddings, top_k=5):
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    similarity_scores = cosine_similarity(
        query_embedding,
        faculty_embeddings
    )[0]

    faculty_df = faculty_df.copy()
    faculty_df["score"] = similarity_scores

    results = (
        faculty_df
        .sort_values("score", ascending=False)
        .head(top_k)
        .reset_index(drop=True)
    )

    return results[
        ["id", "name", "specialization", "profile_url", "score"]
    ]

# =====================================================
# Local testing
# =====================================================
if __name__ == "__main__":
    print("🔹 Loading faculty data")
    faculty_df = load_faculty_data()

    print("🔹 Generating embeddings")
    faculty_embeddings = generate_embeddings(
        faculty_df["semantic_text"].tolist()
    )

    test_query = "faculty working on machine learning in healthcare and data science"

    print(f"\n🔍 Query: {test_query}\n")

    results = recommend_faculty(
        test_query,
        faculty_df,
        faculty_embeddings,
        top_k=5
    )

    print(results)
