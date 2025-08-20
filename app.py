import os
import sys
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

# Add the project root directory to Python path to find the src module
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(PROJECT_ROOT))  # Add the parent directory

# Now we can import from src properly
sys.path.insert(0, PROJECT_ROOT)

# Simple direct imports
from src.resume_processor import extract_text, clean_text
from src.nlp_matcher import match_resumes_to_jobs
from src.candidate_ranker import rank_candidates

# Define allowed extensions here to avoid circular imports
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

app = Flask(__name__,
           template_folder=os.path.join(PROJECT_ROOT, "templates"),
           static_folder=os.path.join(PROJECT_ROOT, "static"))

app.secret_key = "dev-secret-key-123"  # For development only
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and '.' + filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'resumes' not in request.files:
            flash('No resume files uploaded')
            return redirect(request.url)
        
        files = request.files.getlist('resumes')
        job_description = request.form.get('job_description', '').strip()
        
        if not job_description:
            flash('Please provide a job description')
            return redirect(request.url)
        
        if not files or all(file.filename == '' for file in files):
            flash('No selected files')
            return redirect(request.url)

        resumes_text = {}
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                
                try:
                    text = extract_text(filepath)
                    cleaned_text = clean_text(text)
                    resumes_text[filename] = cleaned_text
                except Exception as e:
                    flash(f'Error processing {filename}: {str(e)}')
                    continue
                finally:
                    # Clean up uploaded file
                    if os.path.exists(filepath):
                        os.remove(filepath)

        if not resumes_text:
            flash('No valid resumes were processed')
            return redirect(request.url)

        # Process resumes
        # Create resume objects with text and filename
        resume_objects = [{"text": text, "filename": fname} for fname, text in resumes_text.items()]
        
        # Get match scores with similarity values
        match_scores = match_resumes_to_jobs(resume_objects, job_description)
        
        # Add similarity scores to resume objects for ranking
        for resume_obj in resume_objects:
            for score_obj in match_scores:
                if score_obj.get("text") == resume_obj.get("text"):
                    resume_obj["similarity"] = score_obj.get("similarity", 60.0)
        
        # Rank candidates
        rankings = rank_candidates(resume_objects, job_description)

        return render_template('results.html', results=rankings, job_desc=job_description)

    return render_template('index.html')

if __name__ == '__main__':
    print("Starting Resume Screening System...")
    print(f"Templates directory: {os.path.join(PROJECT_ROOT, 'templates')}")
    print(f"Static directory: {os.path.join(PROJECT_ROOT, 'static')}")
    print("Server running at http://localhost:5000")
    app.run(debug=True, port=5000)
