from flask import Blueprint, request, jsonify
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'recruiter' or 'jobseeker'
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    extracted_text = db.Column(db.Text)
    skills = db.Column(db.JSON)
    experience_years = db.Column(db.Integer)
    education = db.Column(db.JSON)
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class JobDescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.JSON)
    experience_required = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class MatchResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_description.id'), nullable=False)
    match_percentage = db.Column(db.Float, nullable=False)
    missing_skills = db.Column(db.JSON)
    matched_skills = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())