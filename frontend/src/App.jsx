import React, { useState } from 'react';
import Chat from './components/Chat.jsx';

export default function App() {
  const [showSettings, setShowSettings] = useState(false);
  return (
    <div className="app">
      <header className="app__header">
        <h1>Yet Another AI Agent</h1>
        <button onClick={() => setShowSettings(s => !s)} className="btn btn--secondary">{showSettings ? 'Close' : 'Settings'}</button>
      </header>
      {showSettings && (
        <section className="settings">
          <p>Configure environment via VITE_API_BASE_URL.</p>
        </section>
      )}
      <Chat />
      <footer className="app__footer">v0.1.0</footer>
    </div>
  );
}
