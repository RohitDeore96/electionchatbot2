import React, { useState, useRef, useEffect } from 'react';
import { sendChatMessage } from '../services/apiClient';
import { Send, Bot } from 'lucide-react';

/**
 * Chatbot component for Gemini AI.
 * @returns {React.JSX.Element} The rendered GeminiChatbot component.
 */
export default function GeminiChatbot() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { role: 'bot', text: 'Hello! I am your Election Assistant. How can I help you prepare to vote?' }
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const endOfMessagesRef = useRef(null);

  // Auto-scroll to bottom
  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const handleSend = async (e) => {
    e.preventDefault();
    if(!input.trim()) return;
    
    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', text: userMessage }]);
    setIsTyping(true);

    try {
      const data = await sendChatMessage(userMessage);
      setMessages(prev => [...prev, { role: 'bot', text: data.response }]);
    } catch(err) {
      setMessages(prev => [...prev, { role: 'bot', text: "I'm having trouble connecting to the network right now." }]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend(e);
    }
  };

  return (
    <section role="region" aria-labelledby="chat-heading" className="bg-white rounded-xl shadow-sm border border-gray-200 flex flex-col h-[600px] lg:h-full min-h-[500px]">
      <div className="p-4 border-b border-gray-200 bg-neutral-light rounded-t-xl flex items-center">
        <Bot className="w-6 h-6 text-primary mr-2" aria-hidden="true" />
        <h2 id="chat-heading" className="text-xl font-bold text-gray-900">Voter Assistant Chat</h2>
      </div>
      
      <div 
        role="log" 
        aria-live="polite" 
        className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50"
      >
        {messages.map((m, i) => {
          const isUser = m.role === 'user';
          return (
            <div key={i} className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
              <div 
                className={`max-w-[80%] rounded-2xl px-4 py-2 ${
                  isUser 
                    ? 'bg-black text-white rounded-tr-sm' 
                    : 'bg-white border border-black text-black rounded-tl-sm shadow-sm'
                }`}
              >
                <p className="text-sm whitespace-pre-wrap">{m.text}</p>
              </div>
            </div>
          );
        })}
        
        {isTyping && (
          <div className="flex justify-start" role="status" aria-live="polite">
            <div className="bg-white border border-black text-black rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm flex items-center space-x-1">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              <span className="sr-only">Assistant is typing...</span>
            </div>
          </div>
        )}
        <div ref={endOfMessagesRef} />
      </div>

      <div className="p-4 border-t border-gray-200 bg-white rounded-b-xl">
        <form onSubmit={handleSend} aria-label="Chat input form" className="relative flex items-end">
          <label htmlFor="chat-input" className="sr-only">Type a message</label>
          <textarea 
            id="chat-input" 
            value={input} 
            onChange={(e)=>setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your question and press Enter..."
            className="block w-full resize-none border border-gray-300 rounded-xl py-3 pl-4 pr-12 text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-colors bg-neutral-light"
            rows="1"
            required 
          />
          <button 
            type="submit" 
            disabled={!input.trim() || isTyping}
            className="absolute right-2 bottom-1.5 p-1.5 rounded-lg text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50 transition-colors"
            aria-label="Send message"
          >
            <Send className="w-4 h-4" aria-hidden="true" />
          </button>
        </form>
      </div>
    </section>
  );
}
