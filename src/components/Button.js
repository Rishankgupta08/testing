// src/components/Button.js
import React, { useState } from 'react';

function Button() {
  const [theme, setTheme] = useState('light');
  const [isButtonDisabled, setIsButtonDisabled] = useState(false);

  const changeTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  const buttonClick = () => {
    alert('Button clicked!');
  };

  return (
    <div style={{
      backgroundColor: theme === 'light' ? '#f0f0f0' : 'black',
      color: theme === 'light' ? 'black' : 'white',
      fontFamily: 'Arial, sans-serif',
      height: '100vh',
      width: '100vw'
    }}>
      <button
        style={{
          backgroundColor: '#4CAF50',
          color: '#fff',
          padding: '10px 20px',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer'
        }}
        onClick={changeTheme}
      >
        Change Theme
      </button>
      <button
        id="fixedButton"
        style={{
          backgroundColor: '#4CAF50',
          color: '#fff',
          padding: '10px 20px',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer'
        }}
        onClick={buttonClick}
        disabled={isButtonDisabled}
      >
        Fixed Button
      </button>
    </div>
  );
}

export default Button;