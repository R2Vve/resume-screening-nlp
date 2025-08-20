# Resume Screening NLP System

## Overview
A complete resume screening system that:
- Extracts text from PDF, DOCX, and TXT resumes
- Analyzes job descriptions
- Computes semantic similarity with Sentence Transformers
- Extracts skills, experience, and education
- Ranks candidates with a weighted scoring system
- Includes a Flask web interface for uploading resumes and viewing results

## Project Structure
```
resume-screening-nlp/
├── app.py                  # Main Flask application entry point
├── main.py                 # Command-line script for testing
├── requirements.txt        # Project dependencies
├── data/                   # Sample data for testing
│   ├── sample_jobs/        # Sample job descriptions
│   └── sample_resumes/     # Sample resume files
├── src/
│   ├── __init__.py
│   ├── resume_processor.py # Extract text from various resume formats
│   ├── entity_extractor.py # Extract structured information from resumes
│   ├── nlp_matcher.py      # Compute semantic similarity
│   ├── candidate_ranker.py # Rank candidates based on multiple factors
│   ├── skills_db.py        # Reference data for scoring
│   ├── analytics.py        # Analytics functions
│   ├── config.py           # Configuration handling
│   └── database.py         # Database operations
├── static/                 # Static files for web interface
│   └── css/
│       └── style.css
├── templates/              # Flask templates
│   ├── base.html
│   ├── index.html
│   └── results.html
└── tests/                  # Unit tests
    └── test_matching.py
```

## Installation
1. Python 3.9+ recommended
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

## Usage
CLI demo using sample data:
```bash
python main.py
```

Web interface:
```bash
python -m app
# Open http://127.0.0.1:5000 in your browser
```

## Notes
- First run of Sentence Transformers will download the embedding model.
- If spaCy model isn't available, the system falls back to regex-based entity extraction.

## Example Output (CLI)
```
Rank 1: resume1.txt - Final Score: 89.2%
  Matched skills: python, machine learning, pandas, aws
  Experience (years): 5
  Seniority: senior
  Education: masters
Reason: Strong semantic similarity with high skill overlap and sufficient experience.

Rank 2: resume2.txt - Final Score: 77.6%
  Matched skills: python, sql, flask
  Experience (years): 3
  Seniority: mid
  Education: bachelors
Reason: Good similarity and skill match; slightly lower experience than preferred.
```

## License
MIT