# BDE_Project
# FacultyFinder – Big Data Engineering Project

## Project Overview
FacultyFinder is a Big Data Engineering project that builds a complete data pipeline to crawl, clean, store, and serve faculty information from a college website.  
The goal is to prepare structured and clean faculty data that can later be used for semantic search and NLP-based applications.

**Final Objective:**  
Enable a system where a student or researcher can query faculty expertise (e.g., *“Who is working on sustainable energy and carbon capture?”*) even if those exact phrases are not explicitly mentioned in department titles.

---

## Project Architecture

The project follows a standard data engineering lifecycle:

1. **Ingestion (Scraper)**  
   - Scrapes faculty profile pages using Scrapy  
   - Extracts name, bio, specialization, teaching, contact details  
   - Stores raw data in JSON format  

2. **Transformation (Cleaner)**  
   - Cleans and normalizes text using Pandas  
   - Handles missing values and encoding issues  
   - Creates a unified `bio_text` field for NLP tasks  

3. **Storage (Structured Home)**  
   - Stores cleaned data in a SQLite database  
   - Defines a relational schema for persistent storage  

4. **Serving (Hand-off)**  
   - Exposes data through a FastAPI service  
   - Allows downstream Data Scientists to fetch data as JSON  

---


---

## Database Schema

### Table: `faculty`

| Column        | Description |
|--------------|-------------|
| id           | Primary key |
| name         | Faculty name |
| bio          | Biography text |
| specialization | Research interests |
| teaching     | Teaching subjects |
| phone        | Contact number |
| email        | Email address |
| profile_url  | Faculty profile link |
| bio_text     | Combined text used for NLP |

---

## How to Run the Project

### 1️⃣ Run the Scraper
scrapy crawl faculty -o faculty.json

2️⃣ Clean the Data
python transform/clean_faculty.py

3️⃣ Store Data in SQLite
python storage/store_faculty.py

4️⃣ Run the FastAPI Server
uvicorn api.main:app --reload


API Endpoints

GET /all
Returns all faculty records as JSON.

GET /faculty/{id}
Returns details of a single faculty member.

http://127.0.0.1:8000/all
http://127.0.0.1:8000/faculty/1



