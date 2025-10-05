import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import SearchBar from './SearchBar';
import './Navbar.css';

function Navbar({ user, onLogout }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    if (onLogout) onLogout();
    navigate('/');
  };

  const handleSearch = (searchTerm) => {
    navigate(`/career-paths?search=${encodeURIComponent(searchTerm)}`);
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <h2>EduLearn</h2>
        </Link>
        <div className="navbar-menu">
          <SearchBar onSearch={handleSearch} />
          <Link to="/career-paths" className="nav-link">Career Paths</Link>
          <Link to="/skills" className="nav-link">Skills</Link>
          {user ? (
            <>
              <Link to="/dashboard" className="nav-link">Dashboard</Link>
              <Link to="/progress" className="nav-link">My Progress</Link>
              <span className="nav-user">Welcome, {user.username}</span>
              <button onClick={handleLogout} className="btn-logout">Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" className="nav-link">Login</Link>
              <Link to="/register" className="btn-register">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
