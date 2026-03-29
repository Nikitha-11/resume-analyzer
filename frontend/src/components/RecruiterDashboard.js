import React, { useState, useEffect } from 'react';
import { jobAPI } from '../services/api';

const RecruiterDashboard = ({ user }) => {
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [minMatch, setMinMatch] = useState(50);
  const [showJobForm, setShowJobForm] = useState(false);
  const [jobForm, setJobForm] = useState({
    title: '',
    description: '',
    required_skills: '',
    experience_required: 0
  });

  useEffect(() => {
    loadJobs();
  }, []);

  const loadJobs = async () => {
    try {
      const response = await jobAPI.getRecruiterJobs(user.id);
      setJobs(response.data.jobs);
    } catch (error) {
      console.error('Error loading jobs:', error);
    }
  };

  const handleCreateJob = async (e) => {
    e.preventDefault();
    try {
      const jobData = {
        ...jobForm,
        recruiter_id: user.id,
        required_skills: jobForm.required_skills.split(',').map(s => s.trim())
      };
      
      await jobAPI.create(jobData);
      setShowJobForm(false);
      setJobForm({ title: '', description: '', required_skills: '', experience_required: 0 });
      loadJobs();
      alert('Job created successfully!');
    } catch (error) {
      alert('Error creating job: ' + (error.response?.data?.error || 'Unknown error'));
    }
  };

  const loadCandidates = async (jobId) => {
    try {
      // First analyze all resumes for this job
      await jobAPI.analyzeAllResumes(jobId);
      
      // Then get filtered candidates
      const response = await jobAPI.getCandidates(jobId, minMatch);
      setCandidates(response.data.candidates);
      setSelectedJob(jobId);
    } catch (error) {
      console.error('Error loading candidates:', error);
    }
  };

  return (
    <div className="recruiter-dashboard">
      <div className="jobs-section">
        <div className="section-header">
          <h2>Your Job Postings</h2>
          <button onClick={() => setShowJobForm(true)} className="create-job-btn">
            Create New Job
          </button>
        </div>

        {showJobForm && (
          <div className="job-form-modal">
            <form onSubmit={handleCreateJob} className="job-form">
              <h3>Create New Job</h3>
              <input
                type="text"
                placeholder="Job Title"
                value={jobForm.title}
                onChange={(e) => setJobForm({...jobForm, title: e.target.value})}
                required
              />
              <textarea
                placeholder="Job Description"
                value={jobForm.description}
                onChange={(e) => setJobForm({...jobForm, description: e.target.value})}
                required
              />
              <input
                type="text"
                placeholder="Required Skills (comma-separated)"
                value={jobForm.required_skills}
                onChange={(e) => setJobForm({...jobForm, required_skills: e.target.value})}
              />
              <input
                type="number"
                placeholder="Experience Required (years)"
                value={jobForm.experience_required}
                onChange={(e) => setJobForm({...jobForm, experience_required: parseInt(e.target.value)})}
              />
              <div className="form-buttons">
                <button type="submit">Create Job</button>
                <button type="button" onClick={() => setShowJobForm(false)}>Cancel</button>
              </div>
            </form>
          </div>
        )}

        <div className="jobs-grid">
          {jobs.map((job) => (
            <div key={job.id} className="job-card">
              <h3>{job.title}</h3>
              <p>{job.description.substring(0, 100)}...</p>
              <div className="job-skills">
                <strong>Required Skills:</strong>
                {job.required_skills?.map((skill, index) => (
                  <span key={index} className="skill-tag">{skill}</span>
                ))}
              </div>
              <p><strong>Experience:</strong> {job.experience_required} years</p>
              <button 
                onClick={() => loadCandidates(job.id)}
                className="view-candidates-btn"
              >
                View Candidates
              </button>
            </div>
          ))}
        </div>
      </div>

      {selectedJob && (
        <div className="candidates-section">
          <div className="candidates-header">
            <h2>Candidates</h2>
            <div className="filter-controls">
              <label>
                Min Match %:
                <input
                  type="number"
                  value={minMatch}
                  onChange={(e) => setMinMatch(parseInt(e.target.value))}
                  min="0"
                  max="100"
                />
              </label>
              <button onClick={() => loadCandidates(selectedJob)}>
                Apply Filter
              </button>
            </div>
          </div>

          {candidates.length === 0 ? (
            <p>No candidates found matching the criteria.</p>
          ) : (
            <div className="candidates-grid">
              {candidates.map((candidate) => (
                <div key={candidate.resume_id} className="candidate-card">
                  <h4>{candidate.filename}</h4>
                  <div className="match-percentage">
                    <strong>Match: {candidate.match_percentage}%</strong>
                  </div>
                  <p><strong>Experience:</strong> {candidate.experience_years} years</p>
                  
                  <div className="skills-comparison">
                    <div className="matched-skills">
                      <strong>Matched Skills:</strong>
                      {candidate.matched_skills?.map((skill, index) => (
                        <span key={index} className="skill-tag matched">{skill}</span>
                      ))}
                    </div>
                    
                    <div className="missing-skills">
                      <strong>Missing Skills:</strong>
                      {candidate.missing_skills?.map((skill, index) => (
                        <span key={index} className="skill-tag missing">{skill}</span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default RecruiterDashboard;