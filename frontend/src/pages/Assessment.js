import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Assessment.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function Assessment({ user }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [assessment, setAssessment] = useState(null);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    fetchAssessment();
  }, [id, user, navigate]);

  const getAuthHeaders = () => ({
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
  });

  const fetchAssessment = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/assessments/${id}`);
      setAssessment(response.data);
    } catch (error) {
      console.error('Failed to fetch assessment:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (questionId, answer) => {
    setAnswers({ ...answers, [questionId]: answer });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/v1/assessments/${id}/submit`,
        { assessment_id: parseInt(id), answers },
        getAuthHeaders()
      );
      setResult(response.data);
    } catch (error) {
      console.error('Failed to submit assessment:', error);
      alert('Failed to submit assessment');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (!assessment) return <div className="error-message">Assessment not found</div>;
  if (result) {
    return (
      <div className="assessment-page">
        <div className="result-card">
          <h2>Assessment Results</h2>
          <div className="result-score">
            <div className="score-circle">
              <span className="score-percentage">{result.percentage}%</span>
            </div>
            <p>Score: {result.score} / {result.max_score}</p>
          </div>
          <button onClick={() => navigate('/dashboard')} className="btn-primary">
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="assessment-page">
      <div className="assessment-header">
        <h1>{assessment.title}</h1>
        {assessment.description && <p>{assessment.description}</p>}
        {assessment.time_limit && (
          <p className="time-limit">⏱️ Time Limit: {assessment.time_limit} minutes</p>
        )}
      </div>

      <form onSubmit={handleSubmit} className="assessment-form">
        {assessment.questions.map((question, idx) => (
          <div key={question.id} className="question-card">
            <h3>Question {idx + 1}</h3>
            <p className="question-text">{question.question_text}</p>
            
            {question.question_type === 'multiple_choice' && question.options && (
              <div className="options-list">
                {Object.values(question.options).map((option, optIdx) => (
                  <label key={optIdx} className="option-label">
                    <input
                      type="radio"
                      name={`question-${question.id}`}
                      value={option}
                      checked={answers[question.id] === option}
                      onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                      required
                    />
                    <span>{option}</span>
                  </label>
                ))}
              </div>
            )}
            
            {question.question_type === 'true_false' && (
              <div className="options-list">
                <label className="option-label">
                  <input
                    type="radio"
                    name={`question-${question.id}`}
                    value="True"
                    checked={answers[question.id] === 'True'}
                    onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                    required
                  />
                  <span>True</span>
                </label>
                <label className="option-label">
                  <input
                    type="radio"
                    name={`question-${question.id}`}
                    value="False"
                    checked={answers[question.id] === 'False'}
                    onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                    required
                  />
                  <span>False</span>
                </label>
              </div>
            )}
            
            {question.question_type === 'text' && (
              <textarea
                className="text-answer"
                value={answers[question.id] || ''}
                onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                required
                rows={4}
              />
            )}
          </div>
        ))}

        <div className="submit-section">
          <button type="submit" className="btn-primary-large" disabled={submitting}>
            {submitting ? 'Submitting...' : 'Submit Assessment'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default Assessment;
