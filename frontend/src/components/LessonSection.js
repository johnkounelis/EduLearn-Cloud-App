import React from 'react';
import './LessonSection.css';

function LessonSection({ number, title, children, completed = false, onToggleComplete }) {
  return (
    <div className={`lesson-section ${completed ? 'completed' : ''}`}>
      <div className="lesson-header">
        <div className="lesson-number">Lesson {number}</div>
        <h2 className="lesson-title">{title}</h2>
        {onToggleComplete && (
          <button 
            onClick={onToggleComplete}
            className={`complete-checkbox ${completed ? 'checked' : ''}`}
            title={completed ? 'Mark as incomplete' : 'Mark as complete'}
          >
            {completed ? '✓' : ''}
          </button>
        )}
      </div>
      <div className="lesson-content">
        {children}
      </div>
    </div>
  );
}

export default LessonSection;

