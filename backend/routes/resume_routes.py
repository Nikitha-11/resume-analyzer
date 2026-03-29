from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from models.models import Resume, JobDescription, MatchResult, db
from utils.nlp_processor import ResumeProcessor
import os

resume_bp = Blueprint('resume', __name__)
processor = ResumeProcessor()

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@resume_bp.route('/upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    user_id = request.form.get('user_id')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # Process the resume
            result = processor.process_resume(file_path, filename)
            
            # Save to database
            resume = Resume(
                user_id=user_id,
                filename=filename,
                file_path=file_path,
                extracted_text=result['text'],
                skills=result['skills'],
                experience_years=result['experience_years']
            )
            
            db.session.add(resume)
            db.session.commit()
            
            return jsonify({
                'message': 'Resume uploaded and processed successfully',
                'resume_id': resume.id,
                'skills': result['skills'],
                'experience_years': result['experience_years']
            }), 201
            
        except Exception as e:
            return jsonify({'error': f'Error processing resume: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file format'}), 400

@resume_bp.route('/analyze/<int:resume_id>/<int:job_id>', methods=['GET'])
def analyze_resume_job_match(resume_id, job_id):
    resume = Resume.query.get_or_404(resume_id)
    job = JobDescription.query.get_or_404(job_id)
    
    # Calculate match
    match_result = processor.calculate_match_percentage(
        resume.skills or [],
        job.required_skills or []
    )
    
    # Save match result
    match_record = MatchResult(
        resume_id=resume_id,
        job_id=job_id,
        match_percentage=match_result['match_percentage'],
        missing_skills=match_result['missing_skills'],
        matched_skills=match_result['matched_skills']
    )
    
    db.session.add(match_record)
    db.session.commit()
    
    return jsonify({
        'match_percentage': match_result['match_percentage'],
        'matched_skills': match_result['matched_skills'],
        'missing_skills': match_result['missing_skills'],
        'resume_skills': resume.skills,
        'job_skills': job.required_skills
    }), 200

@resume_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_resumes(user_id):
    resumes = Resume.query.filter_by(user_id=user_id).all()
    
    resume_list = []
    for resume in resumes:
        resume_list.append({
            'id': resume.id,
            'filename': resume.filename,
            'skills': resume.skills,
            'experience_years': resume.experience_years,
            'uploaded_at': resume.uploaded_at.isoformat()
        })
    
    return jsonify({'resumes': resume_list}), 200