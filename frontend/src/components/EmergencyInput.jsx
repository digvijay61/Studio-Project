import React, { useState } from 'react';

function EmergencyInput({ onSubmit }) {
  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    
    // Generate random coordinates within our NY mock bounding box
    const lat = 40.7000 + Math.random() * 0.1;
    const lng = -74.0500 + Math.random() * 0.15;
    
    onSubmit(text, lat, lng);
    setText('');
  };

  return (
    <div className="glass-panel animate-fade-in">
      <h3>Report Emergency</h3>
      <form onSubmit={handleSubmit} style={{ marginTop: '15px' }}>
        <input 
          type="text" 
          placeholder="E.g. Two cars crashed on 5th ave..." 
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button type="submit">Deploy AI Dispatch</button>
      </form>
    </div>
  );
}

export default EmergencyInput;
