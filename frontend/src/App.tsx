import { useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import './App.css';

function App() {
  // Redirect to /login when user visits the root URL
  useEffect(() => {
    window.location.href = "/login";
  }, []);

  return <Navigate to="/login" />;
}

export default App;
