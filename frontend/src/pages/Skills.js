import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './Skills.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const LEVEL_ORDER = { beginner: 1, intermediate: 2, advanced: 3, expert: 4 };

function Skills() {
  const [skills, setSkills] = useState([]);
  const [filteredSkills, setFilteredSkills] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSkills();
  }, []);

  useEffect(() => {
    filterSkills();
  }, [skills, selectedCategory, searchTerm]);

  const fetchSkills = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/skills`);
      const data = response.data;
      setSkills(data);
      setFilteredSkills(data);

      // Extract unique categories
      const cats = [...new Set(data.map(s => s.category).filter(Boolean))];
      setCategories(cats.sort());
    } catch (error) {
      console.error('Failed to fetch skills:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterSkills = () => {
    let filtered = skills;

    if (selectedCategory !== 'all') {
      filtered = filtered.filter(s => s.category === selectedCategory);
    }

    if (searchTerm.trim()) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(s =>
        s.name.toLowerCase().includes(term) ||
        s.description?.toLowerCase().includes(term) ||
        s.category?.toLowerCase().includes(term)
      );
    }

    // Sort by level then name
    filtered = [...filtered].sort((a, b) => {
      const levelDiff = (LEVEL_ORDER[a.level] || 0) - (LEVEL_ORDER[b.level] || 0);
      if (levelDiff !== 0) return levelDiff;
      return a.name.localeCompare(b.name);
    });

    setFilteredSkills(filtered);
  };

  const getLevelClass = (level) => {
    switch (level?.toLowerCase()) {
      case 'beginner': return 'level-beginner';
      case 'intermediate': return 'level-intermediate';
      case 'advanced': return 'level-advanced';
      case 'expert': return 'level-expert';
      default: return 'level-beginner';
    }
  };

  return (
    <div className="skills-page">
      <div className="page-header">
        <h1>Skills Library</h1>
        <p>Browse all IT skills and find what you need to learn</p>
      </div>

      <div className="skills-controls">
        <div className="search-section">
          <input
            type="text"
            className="skills-search-input"
            placeholder="Search skills..."
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
      </div>

      {loading ? (
        <div className="loading">Loading skills...</div>
      ) : filteredSkills.length === 0 ? (
        <div className="no-results">
          <p>No skills found matching your search.</p>
          {searchTerm && (
            <button onClick={() => setSearchTerm('')} className="btn-primary">
              Clear Search
            </button>
          )}
        </div>
      ) : (
        <>
          <div className="skills-count">
            Showing {filteredSkills.length} skill{filteredSkills.length !== 1 ? 's' : ''}
          </div>
          <div className="skills-grid">
            {filteredSkills.map((skill) => (
              <div key={skill.id} className="skill-card">
                <div className="skill-card-header">
                  {skill.category && (
                    <span className="skill-category-badge">{skill.category}</span>
                  )}
                  <span className={`skill-level-badge ${getLevelClass(skill.level)}`}>
                    {skill.level}
                  </span>
                </div>
                <h3 className="skill-name">{skill.name}</h3>
                {skill.description && (
                  <p className="skill-description">{skill.description}</p>
                )}
                <div className="skill-card-footer">
                  <Link to="/career-paths" className="btn-explore">
                    Find Career Paths
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default Skills;
