import spacy
import PyPDF2
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import json

from backend.nlp.sbert_model import compute_similarity

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Please install spaCy English model: python -m spacy download en_core_web_sm")

class ResumeProcessor:
    def __init__(self):
        self.skills_database = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js',
            'flask', 'django', 'spring', 'sql', 'mongodb', 'postgresql', 'mysql',
            'aws', 'azure', 'docker', 'kubernetes', 'git', 'machine learning',
            'data science', 'artificial intelligence', 'html', 'css', 'bootstrap'
        ]
    
    def extract_text_from_pdf(self, file_path):
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    
    def extract_text_from_docx(self, file_path):
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def extract_skills(self, text):
        text_lower = text.lower()
        found_skills = []
        for skill in self.skills_database:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        return found_skills
    
    def extract_experience(self, text):
        # Simple regex to find experience years
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'experience\s*:?\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yrs?\s*(?:of\s*)?experience'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return int(match.group(1))
        return 0
    
    '''
    def calculate_match_percentage(self, resume_skills, job_skills):
        if not job_skills:
            return 0
        
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        job_skills_lower = [skill.lower() for skill in job_skills]
        
        matched_skills = list(set(resume_skills_lower) & set(job_skills_lower))
        match_percentage = (len(matched_skills) / len(job_skills_lower)) * 100
        
        missing_skills = list(set(job_skills_lower) - set(resume_skills_lower))
        
        return {
            'match_percentage': round(match_percentage, 2),
            'matched_skills': matched_skills,
            'missing_skills': missing_skills
        }
    '''
    
    def process_resume(self, file_path, filename):
        # Extract text based on file type
        if filename.endswith('.pdf'):
            text = self.extract_text_from_pdf(file_path)
        elif filename.endswith('.docx'):
            text = self.extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format")
        
        # Extract information
        skills = self.extract_skills(text)
        experience = self.extract_experience(text)
        
        return {
            'text': text,
            'skills': skills,
            'experience_years': experience
        }
    
    def calculate_match_percentage(self, resume_skills, job_skills_or_text, job_keywords=None):
        """
        Calculate match percentage using TF-IDF similarity, then adjust with weighted keyword match.
        - resume_skills: list of skills from resume
        - job_skills_or_text: list of skills OR raw job description text
        - job_keywords: optional list of user-provided keywords (uniform weight 1.3)
        """
        # Convert skills lists into text strings for similarity
        resume_text = " ".join(resume_skills) if isinstance(resume_skills, list) else str(resume_skills)
        job_text = " ".join(job_skills_or_text) if isinstance(job_skills_or_text, list) else str(job_skills_or_text)

        # Step 1: TF-IDF similarity
        similarity_score = compute_similarity(resume_text, job_text)
        tfidf_percentage = similarity_score * 100

        # Step 2: Weighted keyword adjustment (if keywords provided)
        final_percentage = tfidf_percentage
        matched_keywords = []
        if job_keywords:
            weight = 1.3
            score = 0
            for kw in job_keywords:
                if kw.lower() in resume_text.lower():
                    matched_keywords.append(kw)
                    score += weight
            max_score = len(job_keywords) * weight
            weighted_percentage = (score / max_score) * 100 if max_score > 0 else 0

        # Combine TF-IDF and weighted keyword score (simple average)
        final_percentage = round((tfidf_percentage + weighted_percentage) / 2, 2)

        # Identify matched and missing skills (basic overlap check)
        matched_skills = list(set(resume_skills) & set(job_skills_or_text)) if isinstance(job_skills_or_text, list) else []
        missing_skills = list(set(job_skills_or_text) - set(resume_skills)) if isinstance(job_skills_or_text, list) else []

        return {
            "match_percentage": round(final_percentage, 2),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
        }
