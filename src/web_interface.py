import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

import sys
import os

# Add src to path if running directly
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.resume_processor import extract_text, clean_text, ALLOWED_EXTENSIONS
from src.nlp_matcher import match_resumes_to_jobs
from src.candidate_ranker import rank_candidates
from database import Database
from config import Config
from analytics import ResumeAnalytics

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(BASE_DIR, "templates")
static_dir = os.path.join(BASE_DIR, "static")
config = Config(os.path.join(BASE_DIR, "config.yml"))

app = Flask(__name__, 
           template_folder=template_dir,
           static_folder=static_dir)
CORS(app)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploaded_resumes")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = Database(config.get("database.path"))
analytics = ResumeAnalytics(db)

def _allowed(filename: str) -> bool:
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        job_desc = request.form.get("job_description", "").strip()
        files = request.files.getlist("resumes")

        if not job_desc:
            flash("Please paste a job description.")
            return redirect(url_for("index"))
        if not files or files[0].filename == "":
            flash("Please upload at least one resume file.")
            return redirect(url_for("index"))

        resume_objs = []
        for file in files:
            if not _allowed(file.filename):
                flash(f"Unsupported file type: {file.filename}")
                continue
            safe_name = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, safe_name)
            file.save(save_path)

            raw = extract_text(save_path)
            cleaned = clean_text(raw)
            if not cleaned:
                flash(f"Could not extract text from {safe_name}")
                continue

            resume_objs.append({"name": safe_name, "text": cleaned})

        if not resume_objs:
            flash("No valid resumes processed.")
            return redirect(url_for("index"))

        matches = match_resumes_to_jobs(resume_objs, job_desc)
        ranked = rank_candidates(matches, job_desc)
        return render_template("results.html", results=ranked, job_desc=job_desc)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)