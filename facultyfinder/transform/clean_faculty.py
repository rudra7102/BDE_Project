import pandas as pd
import re
import os
import json

# -------------------------
# PATHS
# -------------------------
INPUT_PATH = "faculty.json"
OUTPUT_PATH = "data/processed/faculty_clean.csv"

print("Loading raw faculty.json ...")

rows = []
bad_lines = 0

# -------------------------
# LOAD JSON (line-safe)
# -------------------------
with open(INPUT_PATH, "r", encoding="utf-8", errors="ignore") as f:
    for line_no, line in enumerate(f, start=1):
        line = line.strip()

        if not line or line in ["[", "]"]:
            continue

        if line.endswith(","):
            line = line[:-1]

        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                rows.append(obj)
        except json.JSONDecodeError:
            bad_lines += 1

print(f"Valid rows loaded: {len(rows)}")
print(f"Skipped bad lines: {bad_lines}")

# -------------------------
# CREATE DATAFRAME
# -------------------------
df = pd.DataFrame(rows)
print("Columns found:", df.columns.tolist())
print("Rows before cleaning:", len(df))

# -------------------------
# TEXT CLEANER
# -------------------------
def clean_text(text):
    if pd.isna(text) or text is None or str(text).strip() == "":
        return "information not available"
    text = re.sub(r"\s+", " ", str(text))
    return text.strip().lower()

# -------------------------
# ENSURE REQUIRED COLUMNS
# -------------------------
required_cols = [
    "name", "bio", "specialization",
    "teaching", "phone", "email", "profile_url"
]

for col in required_cols:
    if col not in df.columns:
        df[col] = "information not available"

# -------------------------
# CLEAN COLUMNS
# -------------------------
for col in ["name", "bio", "specialization", "phone", "email", "profile_url"]:
    df[col] = df[col].apply(clean_text)

df["teaching"] = df["teaching"].apply(
    lambda x: " ".join(x) if isinstance(x, list) and x else "information not available"
)
df["teaching"] = df["teaching"].apply(clean_text)

# -------------------------
# CREATE SEARCH TEXT
# -------------------------
df["bio_text"] = (
    df["bio"] + " " + df["specialization"] + " " + df["teaching"]
).apply(clean_text)

# -------------------------
# DEDUPLICATION (CRITICAL FIX)
# -------------------------
before = len(df)
df = df.drop_duplicates(subset=["profile_url"])
after = len(df)

print(f"Duplicates removed: {before - after}")
print(f"Final row count: {after}")

# -------------------------
# SAVE (OVERWRITE = SAFE)
# -------------------------
os.makedirs("data/processed", exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

print("✅ CLEAN DATASET WRITTEN TO:", os.path.abspath(OUTPUT_PATH))

# -------------------------
# NULL CHECK (FINAL GUARANTEE)
# -------------------------
print("\nNULL VALUE CHECK:")
print(df.isna().sum())
