import './App.css';
import './styles.css';
import React, { useState } from 'react';
import { predictCandidate } from './api';

function App() {
  const [candidateName, setCandidateName] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  function extractName(filename) {
    const base = filename.split('_')[0];
    return base.toLowerCase();
  }

  function handleFileUpload(event) {
    const file = event.target.files[0];

    if (!file) return;

    setError(''); // clear previous errors

    // 1. Validate extension
    const allowedExtensions = ['.pdf', '.doc', '.docx'];
    const lowerName = file.name.toLowerCase();
    const isAllowed = allowedExtensions.some((ext) => lowerName.endsWith(ext));

    if (!isAllowed) {
      setCandidateName('');
      setResult(null);
      setError('Only PDF, DOC, or DOCX files are allowed.');
      return;
    }

    // 2. Validate filename pattern (example: must contain "_resume")
    if (!lowerName.includes('_resume')) {
      setCandidateName('');
      setResult(null);
      setError("Filename must contain '_resume' (e.g., logan_resume.pdf).");
      return;
    }
    const parsedName = extractName(file.name);

    setCandidateName(parsedName);
    setResult(null);
  }

  async function handlePredict() {
    if (!candidateName) return;

    try {
      setLoading(true);

      const response = await predictCandidate(candidateName);
      console.log('API response:', response);

      setResult(response);
    } catch (err) {
      console.error(err);
      alert('Prediction failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className='container'>
      <h2>Resume Screening</h2>

      <div className='upload-section'>
        <label className='upload-label'>Upload Resume</label>
        <input
          type='file'
          className='upload-input'
          onChange={handleFileUpload}
        />
      </div>
      {error && <p className='error-text'>{error}</p>}
      {/* {candidateName && (
        <p>
          Candidate Name: <strong>{candidateName}</strong>
        </p>
      )} */}

      <button onClick={handlePredict}>Predict Match</button>

      {loading && <div className='spinner'></div>}

      {result && (
        <div
          className={`result ${result.prediction === 1 ? 'success' : 'fail'}`}
        >
          <p>
            Status:{' '}
            <strong>
              {result.prediction === 1
                ? `${candidateName.toUpperCase()} is a good fit for the target role`
                : `${candidateName.toUpperCase()} is not a good fit for the target role`}
            </strong>
          </p>

          <div className='confidence-bar'>
            <div className='confidence-fill' style={{ width: `${100}%` }}></div>
          </div>

          <div className='confidence-section'>
            <p>
              Factors contributing to {candidateName}'s selection prediction:
            </p>
            <ul>
              {Object.entries(result.factors).map(([key, value], index) => (
                <li key={index}>
                  <strong>{key}</strong>: {value}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
