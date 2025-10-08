import React, { useState } from 'react';
import './TryItSection.css';

function TryItSection({ title, type = 'command', command, expectedOutput, onSubmit, hint }) {
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const [isCorrect, setIsCorrect] = useState(null);
  const [showHint, setShowHint] = useState(false);

  const handleSubmit = () => {
    if (type === 'command') {
      const normalized = input.trim().toLowerCase();
      const expected = expectedOutput.trim().toLowerCase();
      const correct = normalized === expected;
      setIsCorrect(correct);
      
      if (correct) {
        setOutput('✓ Correct! Well done.');
      } else {
        setOutput('✗ Incorrect. Try again!');
      }
      
      if (onSubmit) {
        onSubmit(input, correct);
      }
    }
  };

  const handleReset = () => {
    setInput('');
    setOutput('');
    setIsCorrect(null);
    setShowHint(false);
  };

  return (
    <div className="try-it-section">
      <div className="try-it-header">
        <h3>{title || 'Try It Yourself'}</h3>
        <button onClick={handleReset} className="reset-button">Reset</button>
      </div>
      
      <div className="try-it-content">
        {hint && (
          <button 
            onClick={() => setShowHint(!showHint)} 
            className="hint-button"
          >
            {showHint ? 'Hide Hint' : 'Show Hint'}
          </button>
        )}
        
        {showHint && hint && (
          <div className="hint-box">
            💡 {hint}
          </div>
        )}

        {type === 'command' && (
          <>
            <div className="command-prompt">
              <span className="prompt-symbol">$</span>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSubmit()}
                placeholder="Enter command here..."
                className="command-input"
                disabled={isCorrect === true}
              />
            </div>
            
            {output && (
              <div className={`command-output ${isCorrect ? 'success' : 'error'}`}>
                {output}
              </div>
            )}
            
            <button 
              onClick={handleSubmit} 
              className="try-submit-button"
              disabled={!input.trim() || isCorrect === true}
            >
              Run Command
            </button>
          </>
        )}
      </div>
    </div>
  );
}

export default TryItSection;

