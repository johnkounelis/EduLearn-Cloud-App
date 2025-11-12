import React, { useState, useEffect, Component } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import CareerPaths from './pages/CareerPaths';
import CareerPathDetail from './pages/CareerPathDetail';
import Assessment from './pages/Assessment';
import Skills from './pages/Skills';
import Progress from './pages/Progress';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Error Boundary component to catch rendering errors gracefully
class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <h2>Something went wrong</h2>
          <p>Please try refreshing the page.</p>
          <button onClick={() => window.location.reload()} className="btn-primary">
            Refresh Page
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    if (token) {
      // Try to get user info
      axios.get(`${API_BASE_URL}/api/v1/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      }).then(response => {
        setUser(response.data);
      }).catch(() => {
        localStorage.removeItem('token');
      });
    }
    setLoading(false);
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    setUser(null);
  };

  if (loading) {
    return <div className="loading-screen">Loading...</div>;
  }

  return (
    <Router>
      <ErrorBoundary>
      <div className="App">
        <Navbar user={user} onLogout={handleLogout} />
        <main className="App-main">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={user ? <Navigate to="/dashboard" /> : <Login onLogin={handleLogin} />} />
            <Route path="/register" element={user ? <Navigate to="/dashboard" /> : <Register onLogin={handleLogin} />} />
            <Route path="/dashboard" element={user ? <Dashboard user={user} /> : <Navigate to="/login" />} />
            <Route path="/career-paths" element={<CareerPaths />} />
            <Route path="/career-paths/:id" element={<CareerPathDetail user={user} />} />
            <Route path="/skills" element={<Skills />} />
            <Route path="/progress" element={user ? <Progress user={user} /> : <Navigate to="/login" />} />
            <Route path="/assessments/:id" element={user ? <Assessment user={user} /> : <Navigate to="/login" />} />
          </Routes>
        </main>
        <footer className="App-footer">
          <p>&copy; 2024 EduLearn - IT Career Learning Platform. All rights reserved.</p>
        </footer>
      </div>
      </ErrorBoundary>
    </Router>
  );
}

export default App;