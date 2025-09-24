// src/App.js

import React, { useState, useEffect } from 'react';
import './App.css'; // We'll create this file for styling

function App() {
  // --- STATE MANAGEMENT ---
  // Store the user's query
  const [query, setQuery] = useState('');
  // Store the LLM's answer and sources
  const [result, setResult] = useState(null);
  // Store the loading state to show spinners
  const [loading, setLoading] = useState(false);
  // Store the list of indexed files for the sidebar
  const [indexedFiles, setIndexedFiles] = useState([]);

  const [directoryPath, setDirectoryPath] = useState(''); // To hold the value of the new input field
  const [indexing, setIndexing] = useState(false); // To show a loading state specifically for indexing
  const [reindexMessage, setReindexMessage] = useState(''); // To show success/error messages

  const API_URL = 'http://localhost:8000';


  useEffect(() => {
    const fetchIndexedFiles = async () => {
      try {
        const response = await fetch(`/api/indexed-files`);
        const data = await response.json();
        setIndexedFiles(data.files);
      } catch (error) {
        console.error("Failed to fetch indexed files:", error);
      }
    };

    fetchIndexedFiles();
  }, []); // The empty array means this effect runs only once on mount.

  // This function is called when the user submits the search form.
  const handleSearch = async (e) => {
    e.preventDefault(); // Prevent the browser from reloading the page
    if (!query.trim()) return; // Don't search if the query is empty

    setLoading(true);
    setResult(null); // Clear previous results

    try {
      // Make the POST request to the FastAPI backend's /search endpoint
      const response = await fetch(`/api/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Failed to perform search:", error);
      // Display the error to the user
      setResult({ answer: `An error occurred: ${error.message}`, sources: [] });
    } finally {
      setLoading(false);
    }
  };


  const handleReindex = async (e) => {
  e.preventDefault();
  if (!directoryPath.trim()) {
    setReindexMessage('Please enter a directory path.');
    return;
  }

  setIndexing(true);
  setReindexMessage(''); // Clear previous messages

  try {
    const response = await fetch(`${API_URL}/reindex`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ directory_path: directoryPath }),
    });
    
    const data = await response.json();

    if (!response.ok) {
      // If the response has a 'detail' key, it's a FastAPI error
      throw new Error(data.detail || 'Failed to re-index.');
    }
    
    // On success, update the sidebar with the new list of files
    setIndexedFiles(data.indexed_files);
    setReindexMessage(data.message);
  } catch (error) {
    console.error("Failed to re-index:", error);
    setReindexMessage(error.message);
  } finally {
    setIndexing(false);
  }
};

  // --- RENDERED UI (JSX) ---

  return (
    <div className="App">
      <aside className="sidebar">
        <h2>Indexed Files</h2>
        <ul>
          {indexedFiles.length > 0 ? (
            indexedFiles.map((file, index) => <li key={index}>{file}</li>)
          ) : (
            <li>No files indexed.</li>
          )}
        </ul>
        <div className="reindex-container">
    <h3>Switch Directory</h3>
    <form onSubmit={handleReindex}>
      <input
        type="text"
        value={directoryPath}
        onChange={(e) => setDirectoryPath(e.target.value)}
        placeholder="Enter absolute directory path"
        className="reindex-input"
      />
      <button type="submit" className="reindex-button" disabled={indexing}>
        {indexing ? 'Indexing...' : 'Re-index'}
      </button>
    </form>
    {reindexMessage && <p className="reindex-message">{reindexMessage}</p>}
  </div>
      </aside>

      <main className="main-content">
        <header className="App-header">
          <h1>📄 Local RAG Search Engine</h1>
          <p>Ask a question about your documents, and get an AI-powered answer.</p>
        </header>

        <div className="search-container">
          <form onSubmit={handleSearch}>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., What is the recommended model for the contradiction project?"
              className="search-input"
            />
            <button type="submit" className="search-button" disabled={loading}>
              {loading ? 'Searching...' : 'Search'}
            </button>
          </form>
        </div>

        {/* Display the loading spinner or the result */}
        {loading && <div className="spinner"></div>}

        {result && (
          <div className="result-container">
            <h2>Answer</h2>
            <p className="answer-text">{result.answer}</p>
            {result.sources && result.sources.length > 0 && (
              <div className="sources-container">
                <h3>Sources</h3>
                <ul>
                  {result.sources.map((source, index) => (
                    <li key={index}>{source}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;