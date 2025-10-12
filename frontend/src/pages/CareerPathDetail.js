import React, { useState, useEffect, useMemo } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import CodeBlock from '../components/CodeBlock';
import TryItSection from '../components/TryItSection';
import TutorialNavigation from '../components/TutorialNavigation';
import LessonSection from '../components/LessonSection';
import ProgressTracker from '../components/ProgressTracker';
import './CareerPathDetail.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function CareerPathDetail({ user }) {
  const { id } = useParams();
  const [careerPath, setCareerPath] = useState(null);
  const [assessments, setAssessments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [completedSections, setCompletedSections] = useState({});
  const [currentSection, setCurrentSection] = useState(0);

  useEffect(() => {
    fetchCareerPath();
    fetchAssessments();
  }, [id]);

  const fetchCareerPath = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/career-paths/${id}`);
      setCareerPath(response.data);
    } catch (err) {
      setError('Failed to load career path');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchAssessments = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/assessments/career-path/${id}`);
      setAssessments(response.data);
    } catch (err) {
      console.error('Failed to fetch assessments:', err);
    }
  };

  const toggleSectionComplete = (sectionIndex) => {
    setCompletedSections(prev => ({
      ...prev,
      [sectionIndex]: !prev[sectionIndex]
    }));
  };

  const hasLearningContent = careerPath?.learning_content?.lessons?.length > 0;

  const tutorialSections = useMemo(() => {
    if (!careerPath) return [];

    const sections = [
      { title: 'Overview', id: 'overview' },
      { title: 'Required Skills', id: 'skills' },
    ];

    if (hasLearningContent) {
      careerPath.learning_content.lessons.forEach((lesson) => {
        sections.push({
          title: lesson.title,
          id: lesson.title.toLowerCase().replace(/[^a-z0-9]+/g, '-')
        });
      });
    } else {
      sections.push({ title: 'Getting Started', id: 'getting-started' });
    }

    sections.push({ title: 'Practice & Assessment', id: 'assessment' });
    return sections;
  }, [careerPath, hasLearningContent]);

  const completedCount = useMemo(() => Object.values(completedSections).filter(Boolean).length, [completedSections]);
  const totalSections = useMemo(() => tutorialSections.length, [tutorialSections]);

  const renderMarkdownContent = (content) => {
    if (!content) return null;
    const paragraphs = content.split('\n\n');
    return paragraphs.map((para, idx) => {
      // Handle headers
      if (para.startsWith('**') && para.endsWith('**')) {
        return <h3 key={idx}>{para.replace(/\*\*/g, '')}</h3>;
      }

      // Handle bullet lists
      if (para.includes('\n- ')) {
        const lines = para.split('\n');
        const title = lines[0];
        const items = lines.filter(l => l.startsWith('- '));
        return (
          <div key={idx}>
            {title && !title.startsWith('- ') && <p dangerouslySetInnerHTML={{ __html: formatInlineMarkdown(title) }} />}
            <ul>
              {items.map((item, i) => (
                <li key={i} dangerouslySetInnerHTML={{ __html: formatInlineMarkdown(item.replace(/^- /, '')) }} />
              ))}
            </ul>
          </div>
        );
      }

      // Handle numbered lists
      if (/^\d+\.\s/.test(para)) {
        const items = para.split('\n').filter(l => /^\d+\.\s/.test(l));
        return (
          <ol key={idx}>
            {items.map((item, i) => (
              <li key={i} dangerouslySetInnerHTML={{ __html: formatInlineMarkdown(item.replace(/^\d+\.\s/, '')) }} />
            ))}
          </ol>
        );
      }

      // Handle code blocks in content
      if (para.startsWith('```')) {
        const lines = para.split('\n');
        const code = lines.slice(1, -1).join('\n');
        return <CodeBlock key={idx} code={code} language="text" title="Example" />;
      }

      // Regular paragraph
      return <p key={idx} dangerouslySetInnerHTML={{ __html: formatInlineMarkdown(para) }} />;
    });
  };

  const formatInlineMarkdown = (text) => {
    if (!text) return '';
    return text
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/`(.+?)`/g, '<code>$1</code>');
  };

  const getLanguageLabel = (lang) => {
    const labels = {
      'bash': 'Bash',
      'python': 'Python',
      'javascript': 'JavaScript',
      'yaml': 'YAML',
      'hcl': 'Terraform (HCL)',
      'sql': 'SQL',
      'dockerfile': 'Dockerfile',
      'json': 'JSON',
      'groovy': 'Groovy',
    };
    return labels[lang] || lang;
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (error || !careerPath) return <div className="error-message">{error || 'Career path not found'}</div>;

  const lc = careerPath.learning_content;
  let sectionIndex = 0;

  return (
    <div className="career-path-detail-page">
      <div className="breadcrumb">
        <Link to="/">Home</Link> / <Link to="/career-paths">Career Paths</Link> / {careerPath?.title || 'Detail'}
      </div>

      <div className="tutorial-layout">
        <div className="tutorial-sidebar">
          <ProgressTracker
            completed={completedCount}
            total={totalSections}
          />
          <TutorialNavigation
            sections={tutorialSections}
            currentSection={currentSection}
            onSectionClick={setCurrentSection}
          />
        </div>

        <div className="tutorial-main-content">
          <div className="detail-header">
            <div className="header-badges">
              <span className="category-badge">{careerPath.category}</span>
              {careerPath.difficulty && (
                <span className={`difficulty-badge ${careerPath.difficulty.toLowerCase()}`}>
                  {careerPath.difficulty}
                </span>
              )}
            </div>
            <h1>{careerPath.title}</h1>
            <p className="description">{careerPath.description}</p>
          </div>

          <div className="tutorial-content">
            {/* Section: Overview */}
            <div id={`section-${sectionIndex}`}>
              <LessonSection
                number={sectionIndex + 1}
                title="Overview"
                completed={completedSections[sectionIndex]}
                onToggleComplete={() => toggleSectionComplete(sectionIndex)}
              >
                <p>Welcome to the <strong>{careerPath.title}</strong> career path! This comprehensive tutorial will guide you through everything you need to know to start your journey in this field.</p>

                {lc?.overview?.what_youll_learn && (
                  <>
                    <h3>What You'll Learn</h3>
                    <ul>
                      {lc.overview.what_youll_learn.map((item, idx) => (
                        <li key={idx}>{item}</li>
                      ))}
                    </ul>
                  </>
                )}

                {lc?.overview?.prerequisites && (
                  <>
                    <h3>Prerequisites</h3>
                    <ul>
                      {lc.overview.prerequisites.map((item, idx) => (
                        <li key={idx}>{item}</li>
                      ))}
                    </ul>
                  </>
                )}

                <div className="info-grid">
                  {careerPath.estimated_time && (
                    <div className="info-box">
                      <strong>Estimated Time:</strong> {careerPath.estimated_time}
                    </div>
                  )}
                  {careerPath.salary_range && (
                    <div className="info-box">
                      <strong>Salary Range:</strong> {careerPath.salary_range}
                    </div>
                  )}
                </div>

                {(lc?.overview?.career_outlook || careerPath.job_market_info) && (
                  <div className="info-highlight">
                    <h3>Career Outlook</h3>
                    <p>{lc?.overview?.career_outlook || careerPath.job_market_info}</p>
                  </div>
                )}
              </LessonSection>
            </div>

            {/* Section: Required Skills */}
            {(() => { sectionIndex++; return null; })()}
            <div id={`section-${sectionIndex}`}>
              <LessonSection
                number={sectionIndex + 1}
                title="Required Skills"
                completed={completedSections[sectionIndex]}
                onToggleComplete={() => toggleSectionComplete(sectionIndex)}
              >
                <p>To succeed as a <strong>{careerPath.title}</strong>, you'll need to master these essential skills:</p>

                {careerPath.skills && careerPath.skills.length > 0 && (
                  <div className="skills-grid">
                    {careerPath.skills.map((skill, idx) => (
                      <div key={idx} className="skill-card">
                        <div className="skill-header">
                          <span className="skill-name">{skill.name}</span>
                          {skill.level && (
                            <span className={`skill-level ${skill.level}`}>{skill.level}</span>
                          )}
                        </div>
                        {skill.description && (
                          <p className="skill-description">{skill.description}</p>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </LessonSection>
            </div>

            {/* Dynamic Lesson Sections from learning_content */}
            {hasLearningContent ? (
              lc.lessons.map((lesson, lessonIdx) => {
                sectionIndex++;
                return (
                  <div key={lessonIdx} id={`section-${sectionIndex}`}>
                    <LessonSection
                      number={sectionIndex + 1}
                      title={lesson.title}
                      completed={completedSections[sectionIndex]}
                      onToggleComplete={() => toggleSectionComplete(sectionIndex)}
                    >
                      {/* Lesson content */}
                      {lesson.content && (
                        <div className="lesson-text-content">
                          {renderMarkdownContent(lesson.content)}
                        </div>
                      )}

                      {/* Code examples */}
                      {lesson.code_examples && lesson.code_examples.length > 0 && (
                        <div className="code-examples-section">
                          {lesson.code_examples.map((example, codeIdx) => (
                            <div key={codeIdx} className="code-example-block">
                              <CodeBlock
                                code={example.code}
                                language={example.language || 'bash'}
                                title={example.title}
                              />
                            </div>
                          ))}
                        </div>
                      )}

                      {/* Try It section */}
                      {lesson.try_it && (
                        <TryItSection
                          title="Try It Yourself"
                          type="command"
                          expectedOutput={lesson.try_it.command}
                          hint={lesson.try_it.hint}
                        />
                      )}

                      {/* Key takeaways */}
                      {lesson.key_takeaways && lesson.key_takeaways.length > 0 && (
                        <div className="key-takeaways">
                          <h3>Key Takeaways</h3>
                          <ul>
                            {lesson.key_takeaways.map((takeaway, idx) => (
                              <li key={idx}>{takeaway}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </LessonSection>
                  </div>
                );
              })
            ) : (
              /* Fallback: Getting Started section when no learning content */
              (() => {
                sectionIndex++;
                return (
                  <div id={`section-${sectionIndex}`}>
                    <LessonSection
                      number={sectionIndex + 1}
                      title="Getting Started"
                      completed={completedSections[sectionIndex]}
                      onToggleComplete={() => toggleSectionComplete(sectionIndex)}
                    >
                      <p>Let's start learning! Here are the fundamental concepts you need to understand.</p>
                      <h3>Step 1: Understanding the Basics</h3>
                      <p>Before diving into advanced topics, make sure you have a solid foundation. Start with the core concepts and gradually build your knowledge.</p>
                      <h3>Step 2: Hands-On Practice</h3>
                      <p>Practice is essential. Use the interactive exercises below to reinforce what you learn.</p>
                    </LessonSection>
                  </div>
                );
              })()
            )}

            {/* Section: Practice & Assessment */}
            {(() => { sectionIndex++; return null; })()}
            <div id={`section-${sectionIndex}`}>
              <LessonSection
                number={sectionIndex + 1}
                title="Practice & Assessment"
                completed={completedSections[sectionIndex]}
                onToggleComplete={() => toggleSectionComplete(sectionIndex)}
              >
                <p>Now that you've learned the fundamentals, test your knowledge with our assessments!</p>

                {assessments.length > 0 ? (
                  <div className="assessments-list">
                    {assessments.map((assessment) => (
                      <div key={assessment.id} className="assessment-card">
                        <h3>{assessment.title}</h3>
                        {assessment.description && <p>{assessment.description}</p>}
                        {assessment.time_limit && (
                          <p className="assessment-meta">Time limit: {assessment.time_limit} minutes</p>
                        )}
                        {user ? (
                          <Link
                            to={`/assessments/${assessment.id}`}
                            className="btn-primary"
                          >
                            Start Assessment
                          </Link>
                        ) : (
                          <Link to="/login" className="btn-secondary">
                            Login to Start
                          </Link>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <p>No assessments available yet. Check back soon!</p>
                )}
              </LessonSection>
            </div>

            <div className="tutorial-navigation-buttons">
              <button
                className="nav-btn prev-btn"
                disabled={currentSection === 0}
                onClick={() => {
                  setCurrentSection(prev => Math.max(0, prev - 1));
                  document.getElementById(`section-${Math.max(0, currentSection - 1)}`)?.scrollIntoView({ behavior: 'smooth' });
                }}
              >
                Previous
              </button>
              <button
                className="nav-btn next-btn"
                disabled={currentSection === totalSections - 1}
                onClick={() => {
                  setCurrentSection(prev => Math.min(totalSections - 1, prev + 1));
                  document.getElementById(`section-${Math.min(totalSections - 1, currentSection + 1)}`)?.scrollIntoView({ behavior: 'smooth' });
                }}
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CareerPathDetail;
