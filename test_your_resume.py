from src.resume_processor import extract_text, clean_text
from src.entity_extractor import extract_experience_years, extract_entities

# Use our text extraction to analyze a sample string
print("\n--- Testing with a Manually Entered Resume Text ---")
# Let's create a simulated resume text to test with
sample_resume_text = """
John Doe
Software Engineer

SUMMARY
Experienced software engineer with 7+ years of experience in Python development and machine learning.
Skilled in developing AI solutions and data analysis.

EXPERIENCE
Senior Developer, ABC Corp (2020-Present)
- Led team of 5 developers
- 3 years experience with TensorFlow

Data Scientist, XYZ Inc (2018-2020)
- 2 years working on ML models
- Developed NLP solutions

Junior Developer, StartUp Co (2016-2018)
- Gained 2 years hands-on experience
"""

cleaned_text = clean_text(sample_resume_text)

print("\n--- Experience Years Detection ---")
years = extract_experience_years(cleaned_text)
print(f"Detected years of experience: {years}")

print("\n--- All Extracted Entities ---")
entities = extract_entities(cleaned_text)
for key, value in entities.items():
    print(f"{key}: {value}")

print("\n--- Experience Year Matching Patterns ---")
import re
# Pattern 1: "X+ years", "X years", "X yrs", "X+ yrs"
pattern1 = r"(\d{1,2})\s*\+?\s*(?:years|year|yrs|yr)\b"
matches1 = re.findall(pattern1, cleaned_text.lower())
print(f"Pattern 1 matches: {matches1}")

# Pattern 2: "X years of experience in ..."
pattern2 = r"(\d{1,2})\s*\+?\s*years? of experience"
matches2 = re.findall(pattern2, cleaned_text.lower())
print(f"Pattern 2 matches: {matches2}")

print("\n--- Improving the Extraction Function ---")
def improved_extract_experience_years(text: str) -> int:
    t = text.lower()
    years = 0
    
    # Original patterns
    for m in re.findall(r"(\d{1,2})\s*\+?\s*(?:years|year|yrs|yr)\b", t):
        try:
            years = max(years, int(m))
        except ValueError:
            continue
            
    for m in re.findall(r"(\d{1,2})\s*\+?\s*years? of experience", t):
        try:
            years = max(years, int(m))
        except ValueError:
            continue
    
    # Additional patterns
    for m in re.findall(r"experience.{0,30}(\d{1,2})\s*\+?\s*(?:years|year|yrs|yr)", t):
        try:
            years = max(years, int(m))
        except ValueError:
            continue
            
    for m in re.findall(r"(\d{1,2})\s*\+?\s*(?:years|year|yrs|yr).{0,30}experience", t):
        try:
            years = max(years, int(m))
        except ValueError:
            continue
    
    return years

print(f"Improved function result: {improved_extract_experience_years(cleaned_text)}")
