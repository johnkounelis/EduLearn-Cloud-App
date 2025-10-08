import React, { useState } from 'react';
import './CodeBlock.css';

function CodeBlock({ code, language = 'bash', title }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  // Simple syntax highlighting (basic colors)
  const highlightCode = (code, lang) => {
    if (lang === 'bash' || lang === 'shell') {
      return code.split('\n').map((line, idx) => {
        if (line.trim().startsWith('#')) {
          return <span key={idx} className="code-comment">{line}\n</span>;
        } else if (line.trim().startsWith('$') || line.trim().startsWith('>')) {
          return <span key={idx}><span className="code-prompt">{line.substring(0, line.indexOf(' ') + 1)}</span>{line.substring(line.indexOf(' ') + 1)}\n</span>;
        }
        return <span key={idx}>{line}\n</span>;
      });
    }
    return code;
  };

  return (
    <div className="code-block-container">
      {title && <div className="code-block-header">
        <span className="code-block-title">{title}</span>
      </div>}
      <div className="code-block">
        <div className="code-block-actions">
          <button onClick={handleCopy} className="copy-button" title="Copy code">
            {copied ? '✓ Copied!' : 'Copy'}
          </button>
        </div>
        <pre className={`code-content language-${language}`}>
          <code>{highlightCode(code, language)}</code>
        </pre>
      </div>
    </div>
  );
}

export default CodeBlock;

