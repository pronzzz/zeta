import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Skills from './components/Skills';

// Placeholder Home Component
const Home = () => (
  <div className="p-8 text-white">
    <h1 className="text-4xl font-bold mb-4">Welcome to Zeta 🧠</h1>
    <p className="text-xl text-gray-400">Your local autonomous AI agent.</p>
    <div className="mt-8 grid gap-4">
      <div className="p-4 bg-gray-800 rounded">Status: <span className="text-green-400">Online</span></div>
      <div className="p-4 bg-gray-800 rounded">Memory: <span className="text-blue-400">ChromaDB Connected</span></div>
    </div>
  </div>
);

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-gray-950 font-sans">
        {/* Sidebar */}
        <div className="w-64 bg-gray-900 border-r border-gray-800 flex flex-col p-4">
          <div className="text-2xl font-bold text-white mb-8 tracking-wider">ZETA</div>
          <nav className="flex flex-col gap-2">
            <Link to="/" className="text-gray-300 hover:bg-gray-800 px-4 py-2 rounded transition">Dashboard</Link>
            <Link to="/chat" className="text-gray-300 hover:bg-gray-800 px-4 py-2 rounded transition">Chat</Link>
            <Link to="/skills" className="text-gray-300 hover:bg-gray-800 px-4 py-2 rounded transition">Skills</Link>
            <Link to="/settings" className="text-gray-300 hover:bg-gray-800 px-4 py-2 rounded transition">Settings</Link>
          </nav>
        </div>

        {/* content */}
        <div className="flex-1 overflow-auto">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/skills" element={<Skills />} />
            <Route path="/chat" element={<div className="p-8 text-white">Chat Component Coming Soon...</div>} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
