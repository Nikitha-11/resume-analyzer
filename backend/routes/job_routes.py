from flask import Blueprint, request, jsonify
from models.models import JobDescription, Resume, MatchResult, db
from utils.nlp_processor import ResumeProcessor

job_bp = Blueprint('job', __name__)
processor = ResumeProcessor()

@job_bp.route('/create', methods=['POST'])
def create_job():
    data = request.get_json()
    
    job = JobDescription(
        recruiter_id=data['recruiter_id'],
        title=data['title'],
        description=data['description'],
        required_skills=data.get('required_skills', []),
        experience_required=data.get('experience_required', 0)
    )
    
    db.session.add(job)
    db.session.commit()
    
    return jsonify({
        'message': 'Job description created successfully',
        'job_id': job.id
    }), 201

@job_bp.route('/recruiter/<int:recruiter_id>', methods=['GET'])
def get_recruiter_jobs(recruiter_id):
    jobs = JobDescription.query.filter_by(recruiter_id=recruiter_id).all()
    
    job_list = []
    for job in jobs:
        job_list.append({
            'id': job.id,
            'title': job.title,
            'description': job.description,
            'required_skills': job.required_skills,
            'experience_required': job.experience_required,
            'created_at': job.created_at.isoformat()
        })
    
    return jsonify({'jobs': job_list}), 200

@job_bp.route('/<int:job_id>/candidates', methods=['GET'])
def get_job_candidates(job_id):
    # Get match threshold from query params (default 50%)
    min_match = request.args.get('min_match', 50, type=float)
    
    # Get all match results for this job above threshold
    matches = db.session.query(MatchResult, Resume).join(
        Resume, MatchResult.resume_id == Resume.id
    ).filter(
        MatchResult.job_id == job_id,
        MatchResult.match_percentage >= min_match
    ).order_by(MatchResult.match_percentage.desc()).all()
    
    candidates = []
    for match, resume in matches:
        candidates.append({
            'resume_id': resume.id,
            'filename': resume.filename,
            'skills': resume.skills,
            'experience_years': resume.experience_years,
            'match_percentage': match.match_percentage,
            'matched_skills': match.matched_skills,
            'missing_skills': match.missing_skills
        })
    
    return jsonify({
        'candidates': candidates,
        'total_candidates': len(candidates),
        'filter_threshold': min_match
    }), 200

@job_bp.route('/<int:job_id>/analyze-all', methods=['POST'])
def analyze_all_resumes_for_job(job_id):
    job = JobDescription.query.get_or_404(job_id)
    resumes = Resume.query.all()
    
    results = []
    for resume in resumes:
        # Check if match already exists
        existing_match = MatchResult.query.filter_by(
            resume_id=resume.id, 
            job_id=job_id
        ).first()
        
        if not existing_match:
            # Calculate match
            match_result = processor.calculate_match_percentage(
                resume.skills or [],
                job.required_skills or []
            )
            
            # Save match result
            match_record = MatchResult(
                resume_id=resume.id,
                job_id=job_id,
                match_percentage=match_result['match_percentage'],
                missing_skills=match_result['missing_skills'],
                matched_skills=match_result['matched_skills']
            )
            
            db.session.add(match_record)
            results.append({
                'resume_id': resume.id,
                'match_percentage': match_result['match_percentage']
            })
    
    db.session.commit()
    
    return jsonify({
        'message': f'Analyzed {len(results)} resumes',
        'results': results
    }), 200