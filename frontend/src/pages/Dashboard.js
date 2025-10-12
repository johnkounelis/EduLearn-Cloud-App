import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './Dashboard.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function Dashboard({ user }) {
  const [progress, setProgress] = useState([]);
  const [assessments, setAssessments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) {
      fetchProgress();
      fetchAssessments();
    }
  }, [user]);

  const getAuthHeaders = () => ({
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
  });

  const fetchProgress = async () => {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/api/v1/progress`,
        getAuthHeaders()
      );
      setProgress(response.data);
    } catch (error) {
      console.error('Failed to fetch progress:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchAssessments = async () => {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/api/v1/assessments/user/history`,
        getAuthHeaders()
      );
      setAssessments(response.data);
    } catch (error) {
      console.error('Failed to fetch assessments:', error);
    }
  };

  if (!user) {
    return (
      <div className="dashboard-page">
        <div className="welcome-message">
          <h2>Welcome!</h2>
          <p>Please log in to view your dashboard.</p>
          <Link to="/login" className="btn-primary">Login</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <p>Welcome, {user.username}!</p>
      </div>

      <div className="dashboard-content">
        <div className="stats-section">
          <div className="stat-card">
            <h3>Career Paths</h3>
            <div className="stat-number">{progress.length}</div>
            <Link to="/career-paths" className="stat-link">View All →</Link>
          </div>
          <div className="stat-card">
            <h3>Assessments</h3>
            <div className="stat-number">{assessments.length}</div>
            <Link to="/progress" className="stat-link">History →</Link>
          </div>
        </div>

        <div className="progress-section">
          <h2>Progress</h2>
          {loading ? (
            <div className="loading">Loading...</div>
          ) : progress.length > 0 ? (
            <div className="progress-list">
              {progress.map((item) => (
                <div key={item.id} className="progress-item">
                  <div className="progress-header">
                    <span>Career Path #{item.career_path_id}</span>
                    <span>{item.progress_percentage}%</span>
                  </div>
                  <div className="progress-bar">
                    <div 
                      className="progress-fill" 
                      style={{ width: `${item.progress_percentage}%` }}
                    />
                  </div>
                  {item.is_completed && (
                    <span className="completed-badge">✓ Completed</span>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <p>You haven't started any career path yet.</p>
              <Link to="/career-paths" className="btn-primary">
                Explore Career Paths
              </Link>
            </div>
          )}
        </div>

        {assessments.length > 0 && (
          <div className="assessments-section">
            <h2>Recent Assessments</h2>
            <div className="assessments-list">
              {assessments.slice(0, 5).map((assessment) => (
                <div key={assessment.id} className="assessment-result">
                  <div className="result-header">
                    <span>Assessment #{assessment.assessment_id}</span>
                    <span className={`score ${assessment.percentage >= 70 ? 'good' : 'needs-improvement'}`}>
                      {assessment.percentage}%
                    </span>
                  </div>
                  <div className="result-details">
                    Score: {assessment.score}/{assessment.max_score}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
