import React from 'react';
import MapLocator from './components/MapLocator';
import VotingTimeline from './components/VotingTimeline';
import GeminiChatbot from './components/GeminiChatbot';
import './App.css';

function App() {
  return (
    <main className="min-h-screen bg-gray-50 p-6 md:p-12">
      <header className="max-w-5xl mx-auto mb-10 text-center">
        <h1 className="text-4xl font-extrabold text-neutral-dark tracking-tight mb-2">Election Assistant</h1>
        <p className="text-lg text-gray-700">Your interactive guide to the election process.</p>
      </header>
      <div className="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-8">
          <VotingTimeline />
          <MapLocator />
        </div>
        <div>
          <GeminiChatbot />
        </div>
      </div>
    </main>
  );
}

export default App;
