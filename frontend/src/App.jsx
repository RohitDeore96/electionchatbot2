import React, { Suspense, lazy } from 'react';
import VotingTimeline from './components/VotingTimeline';
const MapLocator = lazy(() => import('./components/MapLocator'));
const GeminiChatbot = lazy(() => import('./components/GeminiChatbot'));
import './App.css';

/**
 * Main application component.
 * @returns {React.JSX.Element} The rendered App component.
 */
function App() {
  return (
    <main role="main" className="min-h-screen bg-gray-50 p-6 md:p-12">
      <header className="max-w-5xl mx-auto mb-10 text-center">
        <h1 className="text-4xl font-extrabold text-neutral-dark tracking-tight mb-2">Election Assistant</h1>
        <p className="text-lg text-gray-700">Your interactive guide to the election process.</p>
      </header>
      <section className="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8" aria-label="Main Content">
        <article className="space-y-8">
          <VotingTimeline />
          <Suspense fallback={<div>Loading Map...</div>}>
            <MapLocator />
          </Suspense>
        </article>
        <aside>
          <Suspense fallback={<div>Loading Chatbot...</div>}>
            <GeminiChatbot />
          </Suspense>
        </aside>
      </section>
    </main>
  );
}

export default App;
