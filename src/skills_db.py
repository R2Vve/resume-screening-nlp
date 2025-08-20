# A lightweight skills vocabulary and synonyms for extraction & scoring

SKILL_SYNONYMS = {
    "python": ["python", "py", "python3"],
    "java": ["java"],
    "javascript": ["javascript", "js", "node.js", "nodejs", "typescript", "ts"],
    "sql": ["sql", "postgresql", "mysql", "mssql", "sqlite"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "tensorflow": ["tensorflow", "tf"],
    "pytorch": ["pytorch", "torch"],
    "machine learning": ["machine learning", "ml", "mlops"],
    "deep learning": ["deep learning", "dl", "neural networks"],
    "nlp": ["nlp", "natural language processing", "spacy", "transformers"],
    "data science": ["data science", "data scientist"],
    "aws": ["aws", "amazon web services", "ec2", "s3", "lambda"],
    "gcp": ["gcp", "google cloud", "bigquery"],
    "azure": ["azure", "microsoft azure"],
    "docker": ["docker", "containers"],
    "kubernetes": ["kubernetes", "k8s"],
    "flask": ["flask"],
    "django": ["django"],
    "fastapi": ["fastapi"],
    "airflow": ["airflow"],
    "spark": ["spark", "pyspark"],
    "tableau": ["tableau"],
    "power bi": ["power bi", "powerbi"],
    "excel": ["excel"],
}

# A flattened set of terms for quick matching
CANONICAL_SKILLS = set(SKILL_SYNONYMS.keys())
ALL_SKILL_TERMS = set(term for terms in SKILL_SYNONYMS.values() for term in terms)

EDUCATION_LEVELS = {
    "phd": 5,
    "doctorate": 5,
    "masters": 4,
    "master": 4,
    "mba": 4,
    "bachelors": 3,
    "bachelor": 3,
    "undergraduate": 3,
    "associates": 2,
    "associate": 2,
    "diploma": 1,
    "high school": 1,
}

SENIORITY_KEYWORDS = {
    "intern": ["intern", "internship"],
    "entry": ["entry", "junior", "jr", "graduate"],
    "mid": ["mid", "intermediate", "mid-level"],
    "senior": ["senior", "sr", "lead", "principal", "staff"],
}