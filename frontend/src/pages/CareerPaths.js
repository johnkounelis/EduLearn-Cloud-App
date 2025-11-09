import React, { useState, useEffect, useCallback } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import axios from 'axios';
import './CareerPaths.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function CareerPaths() {
  const [searchParams] = useSearchParams();
  const [careerPaths, setCareerPaths] = useState([]);
  const [filteredPaths, setFilteredPaths] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedDifficulty, setSelectedDifficulty] = useState('all');
  const [searchTerm, setSearchTerm] = useState(searchParams.get('search') || '');

  const filterPaths = useCallback(() => {
    let filtered = careerPaths;

    // Filter by category
    if (selectedCategory !== 'all') {
      filtered = filtered.filter(path => path.category === selectedCategory);
    }

    // Filter by difficulty
    if (selectedDifficulty !== 'all') {
      filtered = filtered.filter(path => path.difficulty?.toLowerCase() === selectedDifficulty.toLowerCase());
    }

    // Filter by search term
    if (searchTerm.trim()) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(path =>
        path.title.toLowerCase().includes(term) ||
        path.description?.toLowerCase().includes(term) ||
        path.category.toLowerCase().includes(term)
      );
    }

    setFilteredPaths(filtered);
  }, [careerPaths, selectedCategory, selectedDifficulty, searchTerm]);

  useEffect(() => {
    fetchCareerPaths();
    fetchCategories();
  }, [selectedCategory]);

  useEffect(() => {
    if (careerPaths.length > 0 || searchTerm || selectedCategory !== 'all' || selectedDifficulty !== 'all') {
      filterPaths();
    } else {
      setFilteredPaths(careerPaths);
    }
  }, [careerPaths, searchTerm, selectedCategory, selectedDifficulty, filterPaths]);

  const fetchCareerPaths = async () => {
    setLoading(true);
    try {
      const url = selectedCategory === 'all' 
        ? `${API_BASE_URL}/api/v1/career-paths`
        : `${API_BASE_URL}/api/v1/career-paths?category=${selectedCategory}`;
      const response = await axios.get(url);
      setCareerPaths(response.data);
      setFilteredPaths(response.data);
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
    <div className="career-paths-page">
      <div className="page-header">
        <h1>Career Paths</h1>
        <p>Explore various careers in IT</p>
      </div>

      <div className="search-and-filters">
        <div className="search-section">
          <input
            type="text"
            className="career-search-input"
            placeholder="Search career paths..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          {searchTerm && (
            <button 
              className="clear-search"
              onClick={() => setSearchTerm('')}
              title="Clear search"
            >
              ✕
            </button>
          )}
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

        <div className="difficulty-filters">
          {['all', 'Beginner', 'Intermediate', 'Advanced'].map(level => (
            <button
              key={level}
              className={selectedDifficulty === level ? 'filter-btn difficulty active' : 'filter-btn difficulty'}
              onClick={() => setSelectedDifficulty(level)}
            >
              {level === 'all' ? 'All Levels' : level}
            </button>
          ))}
        </div>
      </div>

      {!loading && (
        <div className="results-count">
          Showing {filteredPaths.length} of {careerPaths.length} career paths
        </div>
      )}

        {loading ? (
        <div className="loading">Loading career paths...</div>
      ) : filteredPaths.length === 0 ? (
        <div className="no-results">
          <p>No career paths found matching your search.</p>
          {searchTerm && (
            <button onClick={() => setSearchTerm('')} className="btn-primary">
              Clear Search
            </button>
          )}
        </div>
      ) : (
        <div className="career-paths-grid">
          {filteredPaths.map((path) => (
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
    </div>
  );
}

export default CareerPaths;
