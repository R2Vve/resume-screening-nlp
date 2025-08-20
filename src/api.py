from flask import Blueprint, jsonify, request
from typing import Dict, Any
from .database import Database
from .resume_processor import extract_text, clean_text
from .nlp_matcher import match_resumes_to_jobs
from .candidate_ranker import rank_candidates

api = Blueprint('api', __name__)
db = Database()

@api.route('/api/jobs', methods=['POST'])
def create_job():
    """Create a new job posting."""
    data = request.get_json()
    required = data.get('required_skills', [])
    preferred = data.get('preferred_skills', [])
    
    job_id = db.add_job(
        title=data['title'],
        description=data['description'],
        required_skills=required,
        preferred_skills=preferred
    )
    
    return jsonify({'job_id': job_id}), 201

@api.route('/api/candidates', methods=['POST'])
def create_candidate():
    """Add a new candidate with their resume."""
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400
        
    resume_file = request.files['resume']
    resume_text = extract_text(resume_file)
    cleaned_text = clean_text(resume_text)
    
    candidate_id = db.add_candidate(
        name=request.form['name'],
        email=request.form['email'],
        phone=request.form.get('phone', ''),
        resume_text=cleaned_text,
        skills=request.form.getlist('skills'),
        experience_years=int(request.form['experience_years']),
        education_level=request.form['education_level']
    )
    
    return jsonify({'candidate_id': candidate_id}), 201

@api.route('/api/screen', methods=['POST'])
def screen_candidate():
    """Screen a candidate against a job."""
    data = request.get_json()
    job_id = data['job_id']
    candidate_id = data['candidate_id']
    
    # Get job and candidate data from database
    job = db.get_job(job_id)
    candidate = db.get_candidate(candidate_id)
    
    # Perform matching
    similarity_score = match_resumes_to_jobs(
        candidate['resume_text'],
        job['description']
    )
    
    ranking = rank_candidates(
        [candidate],
        job['description'],
        job['required_skills'],
        job['preferred_skills']
    )[0]  # Get first (and only) result
    
    # Store screening result
    screening_id = db.add_screening(
        job_id=job_id,
        candidate_id=candidate_id,
        similarity_score=similarity_score,
        skill_match_score=ranking['skill_match_score'],
        total_score=ranking['total_score'],
        feedback=ranking['reason']
    )
    
    return jsonify({
        'screening_id': screening_id,
        'similarity_score': similarity_score,
        'skill_match_score': ranking['skill_match_score'],
        'total_score': ranking['total_score'],
        'feedback': ranking['reason']
    })
