import os
from src.resume_processor import load_resumes
from src.nlp_matcher import match_resumes_to_jobs
from src.candidate_ranker import rank_candidates

def test_pipeline_smoke():
    resumes = load_resumes("data/sample_resumes")
    assert len(resumes) >= 2
    job_desc_path = "data/sample_jobs/job1.txt"
    assert os.path.exists(job_desc_path)
    with open(job_desc_path, "r", encoding="utf-8") as f:
        job_desc = f.read()
    matches = match_resumes_to_jobs(resumes, job_desc)
    ranked = rank_candidates(matches, job_desc)
    assert len(ranked) == len(resumes)
    assert "final_score" in ranked[0]