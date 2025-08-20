from typing import Dict, List
from sklearn.metrics.pairwise import cosine_similarity

# Lazy-load the sentence transformer model to speed startup
_model = None
MODEL_NAME = "all-MiniLM-L6-v2"

def _ensure_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def get_embedding(text: str):
    model = _ensure_model()
    return model.encode([text])[0]

def match_resumes_to_jobs(resumes, job_description: str) -> List[Dict]:
    """Match resumes to job description using semantic similarity.
    
    Args:
        resumes: Either a list of strings or a list of dictionaries with 'text' key
        job_description: The job description text
        
    Returns:
        List of dictionaries with similarity scores
    """
    job_emb = get_embedding(job_description)
    results: List[Dict] = []
    
    for resume in resumes:
        # Handle both string inputs and dictionary inputs
        if isinstance(resume, dict) and "text" in resume:
            resume_text = resume["text"]
            resume_name = resume.get("filename", "Unknown")
        else:
            resume_text = resume
            resume_name = "Resume"
            
        res_emb = get_embedding(resume_text)
        score = float(cosine_similarity([res_emb], [job_emb])[0][0]) * 100.0
        
        results.append(
            {
                "filename": resume_name,  # Use consistent key name across the application
                "similarity": round(score, 2),
                "text": resume_text,
            }
        )
    return results