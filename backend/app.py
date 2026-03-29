from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume_analyzer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = '../uploads'

db = SQLAlchemy(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Resume Analyzer API is running'})

def create_app():
    # Import routes after app and db are created
    from routes.auth_routes import auth_bp
    from routes.resume_routes import resume_bp
    from routes.job_routes import job_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(resume_bp, url_prefix='/api/resume')
    app.register_blueprint(job_bp, url_prefix='/api/job')
    
    return app

if __name__ == '__main__':
    create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)