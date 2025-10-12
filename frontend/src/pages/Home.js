import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './Home.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function Home() {
  const [careerPaths, setCareerPaths] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('all');

  useEffect(() => {
    fetchCareerPaths();
    fetchCategories();
  }, [selectedCategory]);

  const fetchCareerPaths = async () => {
    try {
      const url = selectedCategory === 'all' 
        ? `${API_BASE_URL}/api/v1/career-paths`
        : `${API_BASE_URL}/api/v1/career-paths?category=${selectedCategory}`;
      const response = await axios.get(url);
      setCareerPaths(response.data);
    } catch (error) {
      console.error('Failed to fetch career paths:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/career-paths/categories/list`);
      setCategories(response.data);
    } catch (error) {
      console.error('Failed to fetch categories:', error);
    }
  };

  return (
    <div className="home-page">
      <section className="hero-section">
        <div className="hero-content">
          <h1>Welcome to EduLearn</h1>
          <p className="hero-subtitle">
            The learning platform for IT graduates and newcomers
          </p>
          <p className="hero-description">
            Learn about various IT fields, required skills, and what you need to know to enter the professional world.
          </p>
          <div className="hero-actions">
            <Link to="/career-paths" className="btn-primary-large">
              Explore Career Paths
            </Link>
            <Link to="/register" className="btn-secondary-large">
              Create Account
            </Link>
          </div>
        </div>
      </section>

      <section className="career-paths-section">
        <div className="section-header">
          <h2>IT Career Paths</h2>
          <p>Choose the career that interests you</p>
        </div>

        <div className="category-filters">
          <button
            className={selectedCategory === 'all' ? 'filter-btn active' : 'filter-btn'}
            onClick={() => setSelectedCategory('all')}
          >
            All
          </button>
          {categories.map(cat => (
            <button
              key={cat}
              className={selectedCategory === cat ? 'filter-btn active' : 'filter-btn'}
              onClick={() => setSelectedCategory(cat)}
            >
              {cat}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="loading">Loading...</div>
        ) : (
          <div className="career-paths-grid">
            {careerPaths.map((path) => (
              <div key={path.id} className="career-path-card">
                <div className="card-header">
                  <span className="category-badge">{path.category}</span>
                  {path.difficulty && (
                    <span className={`difficulty-badge ${path.difficulty.toLowerCase()}`}>
                      {path.difficulty}
                    </span>
                  )}
                </div>
                <h3>{path.title}</h3>
                <p className="card-description">{path.description}</p>
                <div className="card-details">
                  {path.estimated_time && (
                    <div className="detail-item">
                      <span className="detail-label">⏱️ Time:</span>
                      <span>{path.estimated_time}</span>
                    </div>
                  )}
                  {path.salary_range && (
                    <div className="detail-item">
                      <span className="detail-label">💰 Salary:</span>
                      <span>{path.salary_range}</span>
                    </div>
                  )}
                </div>
                <Link to={`/career-paths/${path.id}`} className="btn-primary">
                  Learn More
                </Link>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="features-section">
        <h2>Why EduLearn?</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">🎯</div>
            <h3>Clear Career Paths</h3>
            <p>Learn about different IT fields and their requirements</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Skills Assessment</h3>
            <p>Take quizzes to see your knowledge level</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📈</div>
            <h3>Progress Tracking</h3>
            <p>Track your progress in each career path</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">☁️</div>
            <h3>Cloud & DevOps</h3>
            <p>Specialize in Cloud Architecture and DevOps</p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;
