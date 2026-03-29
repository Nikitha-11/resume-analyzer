import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.nlp_processor import ResumeProcessor

def test_nlp_processor():
    processor = ResumeProcessor()
    
    # Test skill extraction
    sample_text = """
    John Doe
    Software Engineer with 5 years of experience
    Skills: Python, JavaScript, React, SQL, Machine Learning
    """
    
    skills = processor.extract_skills(sample_text)
    experience = processor.extract_experience(sample_text)
    
    print("=== NLP Processor Test ===")
    print(f"Sample text: {sample_text.strip()}")
    print(f"Extracted skills: {skills}")
    print(f"Extracted experience: {experience} years")
    
    # Test match calculation
    resume_skills = ['python', 'javascript', 'react']
    job_skills = ['python', 'react', 'node.js', 'sql']
    
    match_result = processor.calculate_match_percentage(resume_skills, job_skills)
    print(f"\nMatch Analysis:")
    print(f"Resume skills: {resume_skills}")
    print(f"Job skills: {job_skills}")
    print(f"Match percentage: {match_result['match_percentage']}%")
    print(f"Matched skills: {match_result['matched_skills']}")
    print(f"Missing skills: {match_result['missing_skills']}")

if __name__ == "__main__":
    test_nlp_processor()