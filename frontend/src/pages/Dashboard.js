import React, { useState, useEffect } from 'react';
import JobSeekerDashboard from '../components/JobSeekerDashboard';
import RecruiterDashboard from '../components/RecruiterDashboard';

const Dashboard = ({ user, setUser }) => {
  const handleLogout = () => {
    setUser(null);
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Resume Analyzer</h1>
        <div className="user-info">
          <span>Welcome, {user.name} ({user.user_type})</span>
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </div>
      </header>
      
      <main className="dashboard-content">
        {user.user_type === 'jobseeker' ? (
          <JobSeekerDashboard user={user} />
        ) : (
          <RecruiterDashboard user={user} />
        )}
      </main>
    </div>
  );
};

export default Dashboard;