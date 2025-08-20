from src.entity_extractor import extract_experience_years

# Test with sample resumes
with open("data/sample_resumes/resume1.txt", "r", encoding="utf-8") as f:
    resume1_text = f.read()
    
with open("data/sample_resumes/resume2.txt", "r", encoding="utf-8") as f:
    resume2_text = f.read()

print("Resume 1 experience years:", extract_experience_years(resume1_text))
print("Resume 2 experience years:", extract_experience_years(resume2_text))

# Test with some example text patterns
test_strings = [
    "5+ years experience in Python",
    "Experience: 3 years in data science",
    "With 7 years of experience in software development",
    "4 yrs experience in machine learning",
    "8+ yrs of experience with Java",
    "10 years of experience in project management",
]

for i, test in enumerate(test_strings, 1):
    years = extract_experience_years(test)
    print(f"Test {i}: '{test}' → {years} years")
