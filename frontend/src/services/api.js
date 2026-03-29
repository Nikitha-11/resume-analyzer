import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
};

export const resumeAPI = {
  upload: (formData) => api.post('/resume/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getUserResumes: (userId) => api.get(`/resume/user/${userId}`),
  analyzeMatch: (resumeId, jobId) => api.get(`/resume/analyze/${resumeId}/${jobId}`),
};

export const jobAPI = {
  create: (jobData) => api.post('/job/create', jobData),
  getRecruiterJobs: (recruiterId) => api.get(`/job/recruiter/${recruiterId}`),
  getCandidates: (jobId, minMatch = 50) => api.get(`/job/${jobId}/candidates?min_match=${minMatch}`),
  analyzeAllResumes: (jobId) => api.post(`/job/${jobId}/analyze-all`),
};

export default api;