import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import MapLocator from '../src/components/MapLocator';
import GeminiChatbot from '../src/components/GeminiChatbot';
import VotingTimeline from '../src/components/VotingTimeline';
import * as apiClient from '../src/services/apiClient';

jest.mock('../src/services/apiClient', () => ({
  fetchVoterInfo: jest.fn(),
  sendChatMessage: jest.fn()
}));

// Mock window/globals for lucide icons if necessary
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

describe('Components', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('MapLocator searches address', async () => {
    apiClient.fetchVoterInfo.mockResolvedValueOnce({ address: "123 Main St" });
    render(<MapLocator />);
    fireEvent.change(screen.getByPlaceholderText(/e.g. 123 Main St, Anytown/i), { target: { value: '123 Main St' } });
    fireEvent.click(screen.getByText(/Search/i));
    await waitFor(() => expect(screen.getByText(/123 Main St/i)).toBeInTheDocument());
  });

  test('GeminiChatbot sends message', async () => {
    apiClient.sendChatMessage.mockResolvedValueOnce({ response: "Hello Voter" });
    render(<GeminiChatbot />);
    fireEvent.change(screen.getByPlaceholderText(/Type your question and press Enter.../i), { target: { value: 'Hi' } });
    fireEvent.click(screen.getByRole('button', { name: /Send message/i }));
    await waitFor(() => expect(screen.getByText(/Hello Voter/i)).toBeInTheDocument());
  });

  test('VotingTimeline renders and expands', () => {
    render(<VotingTimeline />);
    expect(screen.getByText(/Election Timeline/i)).toBeInTheDocument();
    fireEvent.click(screen.getByText(/Register to Vote/i));
    expect(screen.getByText(/Ensure you are registered to vote at your current address/i)).toBeInTheDocument();
  });
  test('MapLocator handles API error gracefully', async () => {
    // Suppress console.error during expected test error
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    apiClient.fetchVoterInfo.mockRejectedValueOnce(new Error("Network error"));
    
    render(<MapLocator />);
    fireEvent.change(screen.getByPlaceholderText(/e.g. 123 Main St, Anytown/i), { target: { value: '123 Main St' } });
    fireEvent.click(screen.getByText(/Search/i));
    
    // Ensure loading state happens then clears
    expect(screen.getByText(/Searching.../i)).toBeInTheDocument();
    await waitFor(() => expect(screen.queryByText(/Searching.../i)).not.toBeInTheDocument());
    
    consoleSpy.mockRestore();
  });

  test('MapLocator does not search empty string', () => {
    render(<MapLocator />);
    fireEvent.click(screen.getByText(/Search/i));
    expect(apiClient.fetchVoterInfo).not.toHaveBeenCalled();
  });

  test('GeminiChatbot handles enter key', async () => {
    apiClient.sendChatMessage.mockResolvedValueOnce({ response: "Hello Voter" });
    render(<GeminiChatbot />);
    const input = screen.getByPlaceholderText(/Type your question and press Enter.../i);
    fireEvent.change(input, { target: { value: 'Hi' } });
    fireEvent.keyDown(input, { key: 'Enter', code: 'Enter', shiftKey: false });
    
    await waitFor(() => expect(screen.getByText(/Hello Voter/i)).toBeInTheDocument());
  });

  test('GeminiChatbot handles shift+enter (newline)', async () => {
    render(<GeminiChatbot />);
    const input = screen.getByPlaceholderText(/Type your question and press Enter.../i);
    fireEvent.change(input, { target: { value: 'Hi' } });
    fireEvent.keyDown(input, { key: 'Enter', code: 'Enter', shiftKey: true });
    
    expect(apiClient.sendChatMessage).not.toHaveBeenCalled();
  });

  test('GeminiChatbot handles API error gracefully', async () => {
    apiClient.sendChatMessage.mockRejectedValueOnce(new Error("Network down"));
    render(<GeminiChatbot />);
    const input = screen.getByPlaceholderText(/Type your question and press Enter.../i);
    fireEvent.change(input, { target: { value: 'Hi' } });
    fireEvent.click(screen.getByRole('button', { name: /Send message/i }));
    
    await waitFor(() => expect(screen.getByText(/I'm having trouble connecting to the network right now/i)).toBeInTheDocument());
  });

  test('GeminiChatbot does not send empty message', () => {
    render(<GeminiChatbot />);
    fireEvent.click(screen.getByRole('button', { name: /Send message/i }));
    expect(apiClient.sendChatMessage).not.toHaveBeenCalled();
  });

});

