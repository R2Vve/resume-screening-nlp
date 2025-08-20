from typing import List, Dict, Any
import sqlite3
import json
from datetime import datetime
import os

class Database:
    def __init__(self, db_path: str = "resume_screening.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            
            # Create jobs table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    description TEXT,
                    required_skills TEXT,
                    preferred_skills TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create candidates table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS candidates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    phone TEXT,
                    resume_text TEXT,
                    skills TEXT,
                    experience_years INTEGER,
                    education_level TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create screenings table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS screenings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id INTEGER,
                    candidate_id INTEGER,
                    similarity_score FLOAT,
                    skill_match_score FLOAT,
                    total_score FLOAT,
                    feedback TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (job_id) REFERENCES jobs (id),
                    FOREIGN KEY (candidate_id) REFERENCES candidates (id)
                )
            """)
            
            conn.commit()

    def add_job(self, title: str, description: str, required_skills: List[str], 
                preferred_skills: List[str]) -> int:
        """Add a new job posting and return its ID."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO jobs (title, description, required_skills, preferred_skills)
                VALUES (?, ?, ?, ?)
            """, (title, description, 
                  json.dumps(required_skills), 
                  json.dumps(preferred_skills)))
            return cur.lastrowid

    def add_candidate(self, name: str, email: str, phone: str, 
                     resume_text: str, skills: List[str], 
                     experience_years: int, education_level: str) -> int:
        """Add a new candidate and return their ID."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO candidates (name, email, phone, resume_text, 
                                     skills, experience_years, education_level)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, email, phone, resume_text,
                  json.dumps(skills), experience_years, education_level))
            return cur.lastrowid

    def add_screening(self, job_id: int, candidate_id: int, 
                     similarity_score: float, skill_match_score: float,
                     total_score: float, feedback: str) -> int:
        """Record a screening result."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO screenings (job_id, candidate_id, similarity_score,
                                     skill_match_score, total_score, feedback)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (job_id, candidate_id, similarity_score,
                  skill_match_score, total_score, feedback))
            return cur.lastrowid

    def get_candidate_history(self, candidate_id: int) -> List[Dict[str, Any]]:
        """Get screening history for a candidate."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("""
                SELECT s.*, j.title as job_title
                FROM screenings s
                JOIN jobs j ON s.job_id = j.id
                WHERE s.candidate_id = ?
                ORDER BY s.created_at DESC
            """, (candidate_id,))
            return [dict(row) for row in cur.fetchall()]

    def get_job_candidates(self, job_id: int) -> List[Dict[str, Any]]:
        """Get all candidates screened for a specific job."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("""
                SELECT c.*, s.total_score, s.feedback
                FROM candidates c
                JOIN screenings s ON c.id = s.candidate_id
                WHERE s.job_id = ?
                ORDER BY s.total_score DESC
            """, (job_id,))
            return [dict(row) for row in cur.fetchall()]
