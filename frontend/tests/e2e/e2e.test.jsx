import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../../src/App';
import '@testing-library/jest-dom';

/**
 * E2E test for App Component
 */
describe('E2E Chat Test', () => {
  it('types in input, clicks submit, and waits for async response', async () => {
    render(<App />);
    
    const input = screen.getByPlaceholderText(/Ask me about voting/i) || screen.getByRole('textbox');
    const submitButton = screen.getByRole('button', { name: /send/i });
    
    fireEvent.change(input, { target: { value: 'How do I vote?' } });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      const response = screen.getByText(/You can vote/i);
      expect(response).toBeInTheDocument();
    }, { timeout: 3000 });
  });
});
