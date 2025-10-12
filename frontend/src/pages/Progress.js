import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './Progress.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function Progress({ user }) {
  const [progress, setProgress] = useState([]);
  const [assessments, setAssessments] = useState([]);
  const [careerPaths, setCareerPaths] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) {
      fetchData();
    }
  }, [user]);

  const getAuthHeaders = () => ({
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
  });

  const fetchData = async () => {
    try {
      const [progressRes, assessmentsRes, careerPathsRes] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/v1/progress`, getAuthHeaders()),
        axios.get(`${API_BASE_URL}/api/v1/assessments/user/history`, getAuthHeaders()),
        axios.get(`${API_BASE_URL}/api/v1/career-paths`)
      ]);

      setProgress(progressRes.data);
      setAssessments(assessmentsRes.data);

      // Build lookup map for career path names
      const pathMap = {};
      careerPathsRes.data.forEach(cp => {
        pathMap[cp.id] = cp;
      });
      setCareerPaths(pathMap);
    } catch (error) {
      console.error('Failed to fetch progress data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return (
      <div className="progress-page">
        <div className="auth-prompt">
          <h2>Sign in to track your progress</h2>
          <p>Create an account or log in to see your learning journey.</p>
          <div className="auth-buttons">
            <Link to="/login" className="btn-primary">Login</Link>
            <Link to="/register" className="btn-secondary">Register</Link>
          </div>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="progress-page">
        <div className="loading">Loading your progress...</div>
      </div>
    );
  }

  const completedPaths = progress.filter(p => p.is_completed).length;
  const inProgressPaths = progress.filter(p => !p.is_completed).length;
  const avgScore = assessments.length > 0
    ? Math.round(assessments.reduce((sum, a) => sum + a.percentage, 0) / assessments.length)
    : 0;

  return (
    <div className="progress-page">
      <div className="page-header">
        <h1>My Progress</h1>
        <p>Track your learning journey across all career paths</p>
      </div>

      <div className="progress-stats">
        <div className="stat-card stat-completed">
          <div className="stat-number">{completedPaths}</div>
          <div className="stat-label">Completed</div>
        </div>
        <div className="stat-card stat-inprogress">
          <div className="stat-number">{inProgressPaths}</div>
          <div className="stat-label">In Progress</div>
        </div>
        <div className="stat-card stat-assessments">
          <div className="stat-number">{assessments.length}</div>
          <div className="stat-label">Assessments Taken</div>
        </div>
        <div className="stat-card stat-score">
          <div className="stat-number">{avgScore}%</div>
          <div className="stat-label">Avg Score</div>
        </div>
      </div>

      <div className="progress-sections">
        <section className="progress-career-paths">
          <h2>Career Path Progress</h2>
          {progress.length > 0 ? (
            <div className="progress-list">
              {progress.map((item) => {
                const cp = careerPaths[item.career_path_id];
                return (
                  <div key={item.id} className="progress-card">
                    <div className="progress-card-header">
                      <div className="progress-card-info">
                        <h3>
                          <Link to={`/career-paths/${item.career_path_id}`}>
                            {cp ? cp.title : `Career Path #${item.career_path_id}`}
                          </Link>
                        </h3>
                        {cp && <span className="progress-category">{cp.category}</span>}
                      </div>
                      <div className="progress-percentage">
                        {item.progress_percentage}%
                      </div>
                    </div>
                    <div className="progress-bar-container">
                      <div
                        className={`progress-bar-fill ${item.is_completed ? 'completed' : ''}`}
                        style={{ width: `${item.progress_percentage}%` }}
                      />
                    </div>
                    <div className="progress-card-footer">
                      {item.is_completed ? (
                        <span className="status-badge status-completed">Completed</span>
                      ) : (
                        <span className="status-badge status-active">In Progress</span>
                      )}
                      {item.started_at && (
                        <span className="progress-date">
                          Started: {new Date(item.started_at).toLocaleDateString()}
                        </span>
                      )}
                      {item.completed_at && (
                        <span className="progress-date">
                          Completed: {new Date(item.completed_at).toLocaleDateString()}
                        </span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="empty-state">
              <p>You haven't started any career paths yet.</p>
              <Link to="/career-paths" className="btn-primary">Explore Career Paths</Link>
            </div>
          )}
        </section>

        <section className="progress-assessments">
          <h2>Assessment History</h2>
          {assessments.length > 0 ? (
            <div className="assessment-history">
              {assessments.map((a) => (
                <div key={a.id} className="assessment-history-card">
                  <div className="assessment-history-header">
                    <span className="assessment-label">Assessment #{a.assessment_id}</span>
                    <span className={`assessment-score ${a.percentage >= 70 ? 'score-pass' : 'score-fail'}`}>
                      {a.percentage}%
                    </span>
                  </div>
                  <div className="assessment-history-details">
                    <span>Score: {a.score}/{a.max_score}</span>
                    {a.completed_at && (
                      <span>{new Date(a.completed_at).toLocaleDateString()}</span>
                    )}
                  </div>
                  <div className="assessment-bar-container">
                    <div
                      className={`assessment-bar-fill ${a.percentage >= 70 ? 'pass' : 'fail'}`}
                      style={{ width: `${a.percentage}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <p>You haven't taken any assessments yet.</p>
              <Link to="/career-paths" className="btn-primary">Find Assessments</Link>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

export default Progress;
