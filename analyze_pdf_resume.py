import sys
import os
from PyPDF2 import PdfReader
from src.entity_extractor import extract_experience_years

# Function to directly extract text from PDF
def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return ""

# Get resume path from command line
if len(sys.argv) > 1:
    resume_path = sys.argv[1]
    if not os.path.exists(resume_path):
        print(f"File not found: {resume_path}")
        sys.exit(1)
        
    print(f"Analyzing resume: {resume_path}")
    
    # Extract text directly from PDF
    pdf_text = extract_text_from_pdf(resume_path)
    
    if pdf_text:
        print(f"\nExtracted {len(pdf_text)} characters of text")
        print("First 300 characters:")
        print(pdf_text[:300] + "..." if len(pdf_text) > 300 else pdf_text)
        
        # Try to find experience years
        years = extract_experience_years(pdf_text)
        print(f"\nDetected years of experience: {years}")
        
        # Show experience-related text snippets
        print("\nExperience-related snippets:")
        snippets = []
        for line in pdf_text.lower().split("\n"):
            if "year" in line or "experience" in line or "yr" in line:
                snippets.append(line.strip())
        
        for i, snippet in enumerate(snippets, 1):
            print(f"{i}. {snippet}")
    else:
        print("Failed to extract text from PDF")
else:
    print("Please provide a path to your resume PDF file")
    print("Usage: python analyze_pdf_resume.py path/to/your/resume.pdf")
