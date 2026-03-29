import React, { useState } from 'react';
import { authAPI } from '../services/api';

const Login = ({ setUser }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    name: '',
    user_type: 'jobseeker'
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = isLogin 
        ? await authAPI.login({ email: formData.email })
        : await authAPI.register(formData);
      
      setUser(response.data.user);
    } catch (error) {
      alert(error.response?.data?.error || 'An error occurred');
    }
  };

  return (
    <div className="login-container">
      <div className="login-form">
        <h2>{isLogin ? 'Login' : 'Register'}</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Email"
            value={formData.email}
            onChange={(e) => setFormData({...formData, email: e.target.value})}
            required
          />
          
          {!isLogin && (
            <>
              <input
                type="text"
                placeholder="Full Name"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                required
              />
              <select
                value={formData.user_type}
                onChange={(e) => setFormData({...formData, user_type: e.target.value})}
              >
                <option value="jobseeker">Job Seeker</option>
                <option value="recruiter">Recruiter</option>
              </select>
            </>
          )}
          
          <button type="submit">{isLogin ? 'Login' : 'Register'}</button>
        </form>
        
        <p>
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <button 
            type="button" 
            onClick={() => setIsLogin(!isLogin)}
            className="link-button"
          >
            {isLogin ? 'Register' : 'Login'}
          </button>
        </p>
      </div>
    </div>
  );
};

export default Login;