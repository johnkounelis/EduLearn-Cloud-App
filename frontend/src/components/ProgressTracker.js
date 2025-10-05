import React from 'react';
import './ProgressTracker.css';

function ProgressTracker({ completed, total, showPercentage = true }) {
  const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;

  return (
    <div className="progress-tracker">
      <div className="progress-info">
        <span className="progress-label">Progress</span>
        {showPercentage && (
          <span className="progress-percentage">{percentage}%</span>
        )}
      </div>
      <div className="progress-bar-container">
        <div 
          className="progress-bar-fill"
          style={{ width: `${percentage}%` }}
        />
      </div>
      <div className="progress-stats">
        {completed} of {total} sections completed
      </div>
    </div>
  );
}

export default ProgressTracker;

