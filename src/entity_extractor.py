from typing import Dict, List, Set, Tuple, Optional
import re

# spaCy is optional; fallback to regex if not available
try:
    import spacy
    _NLP = spacy.load("en_core_web_sm")
except Exception:
    _NLP = None

from src.skills_db import SKILL_SYNONYMS, CANONICAL_SKILLS, ALL_SKILL_TERMS, EDUCATION_LEVELS, SENIORITY_KEYWORDS

def _normalize(text: str) -> str:
    return text.lower()

def extract_skills(text: str) -> List[str]:
    t = _normalize(text)
    found: Set[str] = set()
    # Match any synonym term as a whole word
    for canonical, terms in SKILL_SYNONYMS.items():
        for term in terms:
            if re.search(rf"\b{re.escape(term)}\b", t):
                found.add(canonical)
                break
    return sorted(found)

def extract_experience_years(text: str) -> int:
    t = _normalize(text)
    years = 0
    # Pattern examples: "5+ years", "3 years", "2 yrs", "7+ yrs"
    for m in re.findall(r"(\d{1,2})\s*\+?\s*(?:years|year|yrs|yr)\b", t):
        try:
            years = max(years, int(m))
        except ValueError:
            continue
    # Sometimes "X years of experience in ..." phrasing
    for m in re.findall(r"(\d{1,2})\s*\+?\s*years? of experience", t):
        try:
            years = max(years, int(m))
        except ValueError:
            continue
    return years

def detect_seniority(text: str) -> Optional[str]:
    t = _normalize(text)
    order = ["intern", "entry", "mid", "senior"]
    for level in reversed(order):  # prioritize senior if multiple found
        for kw in SENIORITY_KEYWORDS[level]:
            if re.search(rf"\b{re.escape(kw)}\b", t):
                return level
    return None

def extract_education_level(text: str) -> Optional[str]:
    t = _normalize(text)
    best_level = None
    best_score = -1
    for level, score in EDUCATION_LEVELS.items():
        if re.search(rf"\b{re.escape(level)}\b", t):
            if score > best_score:
                best_level = level
                best_score = score
    return best_level

def extract_entities(text: str) -> Dict:
    # Optional spaCy usage to augment extraction (titles, orgs)
    orgs = set()
    if _NLP:
        try:
            doc = _NLP(text)
            orgs = {ent.text for ent in doc.ents if ent.label_ == "ORG"}
        except Exception:
            orgs = set()

    skills = extract_skills(text)
    years = extract_experience_years(text)
    seniority = detect_seniority(text)
    education = extract_education_level(text)

    return {
        "skills": skills,
        "experience_years": years,
        "seniority": seniority,
        "education": education,
        "organizations": sorted(orgs),
    }