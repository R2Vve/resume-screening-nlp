import os
import sys

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.resume_processor import load_resumes
from src.nlp_matcher import match_resumes_to_jobs
from src.candidate_ranker import rank_candidates

def main():
    resumes = load_resumes("data/sample_resumes")
    with open("data/sample_jobs/job1.txt", "r", encoding="utf-8") as f:
        job_desc = f.read()

    match_results = match_resumes_to_jobs(resumes, job_desc)
    ranked = rank_candidates(match_results, job_desc)

    for i, cand in enumerate(ranked, 1):
        print(f"Rank {i}: {cand['filename']} - Final Score: {cand['final_score']}%")
        print(f"  Similarity: {cand['similarity']}%")
        print(f"  Matched skills: {', '.join(cand['matched_skills']) if cand['matched_skills'] else '—'}")
        print(f"  Experience (years): {cand['experience_years']}")
        print(f"  Seniority: {cand['seniority'] or '—'}")
        print(f"  Education: {cand['education'] or '—'}")
        print(f"  Reason: {cand['reason']}\n")

if __name__ == "__main__":
    main()