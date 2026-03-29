# AI-Powered Resume Analyzer

A full-stack web application for recruitment that analyzes resumes against job descriptions using NLP and provides match percentages and skill gap analysis.

## Features

### For Job Seekers:
- Upload resumes (PDF/DOCX)
- Automatic skill extraction
- Experience years detection
- View extracted skills and information

### For Recruiters:
- Create job descriptions with required skills
- Analyze all resumes against job requirements
- Filter candidates by match percentage
- View matched and missing skills for each candidate

## Tech Stack

- **Frontend**: React.js with modern UI
- **Backend**: Python Flask with RESTful APIs
- **NLP**: spaCy for text processing and skill extraction
- **Database**: SQLite (development) / PostgreSQL (production)
- **File Processing**: PyPDF2 for PDFs, python-docx for Word documents

## Project Structure

```
Resume_analyser/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── models/models.py    # Database models
│   ├── routes/             # API routes
│   ├── utils/              # NLP processing utilities
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   └── services/       # API services
│   └── package.json        # Node.js dependencies
├── uploads/                # Resume file storage
└── database/              # Database files
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Quick Setup
1. Run the setup script:
   ```bash
   setup.bat
   ```

### Manual Setup

#### Backend Setup
1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download spaCy English model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

#### Frontend Setup
1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

## Running the Application

### Start Backend Server
```bash
cd backend
python app.py
```
Backend will run on http://localhost:5000

### Start Frontend Server
```bash
cd frontend
npm start
```
Frontend will run on http://localhost:3000

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login

### Resume Management
- `POST /api/resume/upload` - Upload resume file
- `GET /api/resume/user/{user_id}` - Get user's resumes
- `GET /api/resume/analyze/{resume_id}/{job_id}` - Analyze resume-job match

### Job Management
- `POST /api/job/create` - Create job description
- `GET /api/job/recruiter/{recruiter_id}` - Get recruiter's jobs
- `GET /api/job/{job_id}/candidates` - Get filtered candidates
- `POST /api/job/{job_id}/analyze-all` - Analyze all resumes for job

## Usage Flow

### For Job Seekers:
1. Register/Login as job seeker
2. Upload resume (PDF or DOCX)
3. View extracted skills and experience
4. System automatically processes and stores resume data

### For Recruiters:
1. Register/Login as recruiter
2. Create job descriptions with required skills
3. Click "View Candidates" to analyze all resumes
4. Filter candidates by minimum match percentage
5. Review matched and missing skills for each candidate

## NLP Features

- **Text Extraction**: Supports PDF and DOCX formats
- **Skill Detection**: Matches against predefined skill database
- **Experience Extraction**: Uses regex patterns to find years of experience
- **Match Calculation**: Computes percentage based on skill overlap
- **Skill Gap Analysis**: Identifies missing skills for candidates

## Database Schema

- **Users**: Store user information and type (recruiter/jobseeker)
- **Resumes**: Store resume files and extracted information
- **JobDescriptions**: Store job postings and requirements
- **MatchResults**: Store analysis results and match percentages

## Future Enhancements

- AI-powered skill extraction using transformers
- Resume ranking algorithms
- Email notifications for recruiters
- Advanced filtering options
- Resume parsing improvements
- Integration with job boards
- Bulk resume processing
- Analytics dashboard

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

This project is licensed under the MIT License.