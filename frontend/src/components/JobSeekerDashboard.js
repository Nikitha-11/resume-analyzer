import React, { useState, useEffect } from 'react';
import { resumeAPI } from '../services/api';

const JobSeekerDashboard = ({ user }) => {
  const [resumes, setResumes] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    loadResumes();
  }, []);

  const loadResumes = async () => {
    try {
      const response = await resumeAPI.getUserResumes(user.id);
      setResumes(response.data.resumes);
    } catch (error) {
      console.error('Error loading resumes:', error);
    }
  };

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('user_id', user.id);

    try {
      await resumeAPI.upload(formData);
      setSelectedFile(null);
      loadResumes();
      alert('Resume uploaded successfully!');
    } catch (error) {
      alert('Error uploading resume: ' + (error.response?.data?.error || 'Unknown error'));
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="jobseeker-dashboard">
      <div className="upload-section">
        <h2>Upload Resume</h2>
        <form onSubmit={handleFileUpload}>
          <input
            type="file"
            accept=".pdf,.docx"
            onChange={(e) => setSelectedFile(e.target.files[0])}
          />
          <button type="submit" disabled={!selectedFile || uploading}>
            {uploading ? 'Uploading...' : 'Upload Resume'}
          </button>
        </form>
      </div>

      <div className="resumes-section">
        <h2>Your Resumes</h2>
        {resumes.length === 0 ? (
          <p>No resumes uploaded yet.</p>
        ) : (
          <div className="resumes-grid">
            {resumes.map((resume) => (
              <div key={resume.id} className="resume-card">
                <h3>{resume.filename}</h3>
                <p><strong>Experience:</strong> {resume.experience_years} years</p>
                <div className="skills-section">
                  <strong>Skills Found:</strong>
                  <div className="skills-list">
                    {resume.skills?.map((skill, index) => (
                      <span key={index} className="skill-tag">{skill}</span>
                    ))}
                  </div>
                </div>
                <p className="upload-date">
                  Uploaded: {new Date(resume.uploaded_at).toLocaleDateString()}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default JobSeekerDashboard;