import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import App from '../src/App'

test('renders header brand', () => {
  render(<BrowserRouter><App /></BrowserRouter>)
  expect(screen.getByText(/AI Shop/i)).toBeInTheDocument()
})
