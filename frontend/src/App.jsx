import React, { useState } from 'react';

export default function App() {
  const [showSettings, setShowSettings] = useState(false);
  return (
    <div className="app">
      <header className="app__header">
        <h1>Yet Another AI Agent</h1>
      </header>
      <footer className="app__footer">v0.1.0</footer>
    </div>
  );
}
