from typing import Dict, List, Optional
from src.entity_extractor import (
    extract_entities,
    extract_skills,
    extract_experience_years,
    detect_seniority,
    extract_education_level,
)
from src.skills_db import EDUCATION_LEVELS

def _education_score(level: Optional[str]) -> int:
    if level is None:
        return 0
    return EDUCATION_LEVELS.get(level, 0)

def _required_experience(job_text: str) -> int:
    # Extract minimum years required from job description (heuristic)
    years = extract_experience_years(job_text)
    return years

def _job_requirements(job_text: str):
    return {
        "skills": set(extract_skills(job_text)),
        "seniority": detect_seniority(job_text),
        "education_level": extract_education_level(job_text),
        "min_years": _required_experience(job_text),
    }

def rank_candidates(match_results: List[Dict], job_description: str) -> List[Dict]:
    """Rank candidates based on their match to job requirements.
    
    Args:
        match_results: List of dicts with 'text' and 'filename' or 'name' keys
        job_description: The job description text
        
    Returns:
        List of ranked candidate dicts with scores
    """
    req = _job_requirements(job_description)
    req_skills = req["skills"]
    req_seniority = req["seniority"]
    req_edu = req["education_level"]
    req_years = req["min_years"]

    ranked: List[Dict] = []
    for item in match_results:
        ents = extract_entities(item["text"])
        cand_skills = set(ents["skills"])
        cand_years = ents["experience_years"]
        cand_seniority = ents["seniority"]
        cand_edu = ents["education"]

        # Get similarity score, defaulting to 60.0 if not provided
        base = item.get("similarity", 60.0)  # 0..100

        # Skills bonus: overlap proportion relative to job requirements
        skills_bonus = 0.0
        matched_skills = sorted(req_skills & cand_skills)
        if req_skills:
            overlap_ratio = len(matched_skills) / max(1, len(req_skills))
            skills_bonus = overlap_ratio * 20.0  # up to +20

        # Experience bonus: meet/exceed requirement
        exp_bonus = 0.0
        if req_years:
            if cand_years >= req_years:
                # proportional up to +10
                exp_bonus = min(10.0, (cand_years - req_years + 1) * 2.5)
            else:
                # small penalty if under-qualified
                exp_bonus = -min(10.0, (req_years - cand_years) * 2.0)

        # Seniority bonus: exact match +5
        seniority_bonus = 0.0
        if req_seniority and cand_seniority and req_seniority == cand_seniority:
            seniority_bonus = 5.0

        # Education bonus: if candidate meets or exceeds target
        edu_bonus = 0.0
        if req_edu:
            if _education_score(cand_edu) >= _education_score(req_edu):
                edu_bonus = 5.0

        final_score = max(0.0, min(100.0, base + skills_bonus + exp_bonus + seniority_bonus + edu_bonus))

        # Get name from either "name" or "filename" key
        resume_name = item.get("name", item.get("filename", "Unknown Resume"))
        
        ranked.append(
            {
                "filename": resume_name,  # Use consistent key name
                "similarity": round(base, 2),
                "final_score": round(final_score, 2),
                "matched_skills": matched_skills,
                "all_skills": sorted(cand_skills),
                "experience_years": cand_years,
                "seniority": cand_seniority,
                "education": cand_edu,
                "reason": _build_reason(base, matched_skills, cand_years, req_years),
            }
        )

    ranked.sort(key=lambda x: x["final_score"], reverse=True)
    return ranked

def _build_reason(base: float, matched_skills: List[str], cand_years: int, req_years: int) -> str:
    parts = []
    if base >= 80:
        parts.append("Strong semantic similarity")
    elif base >= 60:
        parts.append("Good semantic similarity")
    else:
        parts.append("Moderate semantic similarity")
    if matched_skills:
        parts.append(f"skill overlap: {', '.join(matched_skills)}")
    if req_years:
        if cand_years >= req_years:
            parts.append(f"experience meets requirement ({cand_years}y ≥ {req_years}y)")
        else:
            parts.append(f"experience below requirement ({cand_years}y < {req_years}y)")
    return "; ".join(parts) + "."