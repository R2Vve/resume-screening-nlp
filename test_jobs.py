import os
import sys

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.resume_processor import load_resumes
from src.nlp_matcher import match_resumes_to_jobs
from src.candidate_ranker import rank_candidates

def test_job(job_file):
    """Process a single job file against sample resumes."""
    print(f"\n==================================================")
    print(f"Testing Job Description: {job_file}")
    print(f"==================================================")
    
    # Get absolute paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    resumes_dir = os.path.join(base_dir, "data", "sample_resumes")
    job_path = os.path.join(base_dir, "data", "sample_jobs", job_file)
    
    # Load resumes
    resumes = load_resumes(resumes_dir)
    print(f"Loaded {len(resumes)} sample resumes")
    
    # Load job description
    with open(job_path, "r", encoding="utf-8") as f:
        job_desc = f.read()
        
    # Print the first 150 characters of the job description
    print(f"Excerpt: {job_desc[:150]}...\n")

    # Match and rank
    match_results = match_resumes_to_jobs(resumes, job_desc)
    ranked = rank_candidates(match_results, job_desc)

    # Print results
    for i, cand in enumerate(ranked, 1):
        print(f"Rank {i}: {cand['filename']} - Final Score: {cand['final_score']}%")
        print(f"  Similarity: {cand['similarity']}%")
        print(f"  Matched skills: {', '.join(cand['matched_skills']) if cand['matched_skills'] else '—'}")
        print(f"  Experience (years): {cand['experience_years']}")
        print(f"  Seniority: {cand['seniority'] or '—'}")
        print(f"  Education: {cand['education'] or '—'}")
        print(f"  Reason: {cand['reason']}")

# Test each job file individually
test_job("job2.txt")
test_job("job3.txt")
test_job("job4.txt")
