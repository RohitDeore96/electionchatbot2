import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

test('renders App successfully', () => {
  render(<App />);
  expect(screen.getByText('Election Assistant')).toBeInTheDocument();
});
