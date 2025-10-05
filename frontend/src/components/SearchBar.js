import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './SearchBar.css';

function SearchBar({ onSearch, placeholder = "Search career paths..." }) {
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      if (onSearch) {
        onSearch(searchTerm);
      } else {
        // Default: navigate to career paths with search
        navigate(`/career-paths?search=${encodeURIComponent(searchTerm)}`);
      }
      setSearchTerm('');
    }
  };

  const handleChange = (e) => {
    setSearchTerm(e.target.value);
  };

  return (
    <form className="search-bar" onSubmit={handleSubmit}>
      <input
        type="text"
        className="search-input"
        placeholder={placeholder}
        value={searchTerm}
        onChange={handleChange}
      />
      <button type="submit" className="search-button" title="Search">
        🔍
      </button>
    </form>
  );
}

export default SearchBar;

