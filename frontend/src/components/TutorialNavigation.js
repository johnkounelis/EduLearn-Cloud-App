import React, { useState } from 'react';
import './TutorialNavigation.css';

function TutorialNavigation({ sections, currentSection, onSectionClick }) {
  const [isExpanded, setIsExpanded] = useState(true);

  return (
    <div className={`tutorial-nav ${!isExpanded ? 'collapsed' : ''}`}>
      <div className="tutorial-nav-header">
        <h3>Table of Contents</h3>
        <button 
          onClick={() => setIsExpanded(!isExpanded)}
          className="toggle-nav"
          title={isExpanded ? 'Collapse' : 'Expand'}
        >
          {isExpanded ? '−' : '+'}
        </button>
      </div>
      
      {isExpanded && (
        <nav className="tutorial-nav-list">
          {sections.map((section, index) => (
            <a
              key={index}
              href={`#section-${index}`}
              onClick={(e) => {
                e.preventDefault();
                if (onSectionClick) {
                  onSectionClick(index);
                } else {
                  const element = document.getElementById(`section-${index}`);
                  if (element) {
                    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
                  }
                }
              }}
              className={`nav-item ${currentSection === index ? 'active' : ''}`}
            >
              <span className="nav-number">{index + 1}</span>
              <span className="nav-text">{section.title}</span>
            </a>
          ))}
        </nav>
      )}
    </div>
  );
}

export default TutorialNavigation;

