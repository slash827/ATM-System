// App component integration tests
// Run these tests with: npm test App.test.tsx

import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import App from './App'

describe('App Integration Tests', () => {
  test('renders home page initially', () => {
    render(<App />)
    
    expect(screen.getByText('Welcome to ATM System')).toBeInTheDocument()
    expect(screen.getByText('Your secure banking solution for all your financial needs.')).toBeInTheDocument()
    expect(screen.getByText('Get Started')).toBeInTheDocument()
  })

  test('shows available services on home page', () => {
    render(<App />)
    
    expect(screen.getByText('Available Services')).toBeInTheDocument()
    expect(screen.getByText('Balance Inquiry')).toBeInTheDocument()
    expect(screen.getByText('Cash Withdrawal')).toBeInTheDocument()
    expect(screen.getByText('Deposit Funds')).toBeInTheDocument()
  })

  test('shows demo mode status', () => {
    render(<App />)
    
    expect(screen.getByText('Demo Mode Active')).toBeInTheDocument()
    expect(screen.getByText(/Frontend successfully connected to FastAPI backend/)).toBeInTheDocument()
  })

  test('navigates to account input when Get Started is clicked', () => {
    render(<App />)
    
    const getStartedButton = screen.getByText('Get Started')
    fireEvent.click(getStartedButton)
    
    expect(screen.getByText('Enter Account Number')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('123456')).toBeInTheDocument()
  })

  test('complete user flow: home -> account input -> operations', async () => {
    render(<App />)
    
    // Start from home page
    expect(screen.getByText('Welcome to ATM System')).toBeInTheDocument()
    
    // Click Get Started
    fireEvent.click(screen.getByText('Get Started'))
    
    // Now on account input page
    expect(screen.getByText('Enter Account Number')).toBeInTheDocument()
    
    // Enter valid account number
    const input = screen.getByPlaceholderText('123456')
    fireEvent.change(input, { target: { value: '123456' } })
    
    // Submit form
    const continueButton = screen.getByText('Continue')
    expect(continueButton).not.toBeDisabled()
    fireEvent.click(continueButton)
    
    // Should now be on operations page
    await waitFor(() => {
      expect(screen.getByText('Welcome, Account 123456')).toBeInTheDocument()
    })
    
    expect(screen.getByText('Choose an operation to continue.')).toBeInTheDocument()
    expect(screen.getByText('Check Balance')).toBeInTheDocument()
    expect(screen.getByText('Withdraw Money')).toBeInTheDocument()
    expect(screen.getByText('Deposit Money')).toBeInTheDocument()
  })

  test('can navigate back to home from operations page', async () => {
    render(<App />)
    
    // Navigate to operations page
    fireEvent.click(screen.getByText('Get Started'))
    const input = screen.getByPlaceholderText('123456')
    fireEvent.change(input, { target: { value: '123456' } })
    fireEvent.click(screen.getByText('Continue'))
    
    // Wait for operations page
    await waitFor(() => {
      expect(screen.getByText('Welcome, Account 123456')).toBeInTheDocument()
    })
    
    // Click back to home
    fireEvent.click(screen.getByText('Back to Home'))
    
    // Should be back on home page
    expect(screen.getByText('Welcome to ATM System')).toBeInTheDocument()
    expect(screen.getByText('Get Started')).toBeInTheDocument()
  })

  test('validates account input before proceeding', async () => {
    render(<App />)
    
    // Navigate to account input
    fireEvent.click(screen.getByText('Get Started'))
    
    // Try to submit without entering account number
    fireEvent.click(screen.getByText('Continue'))
    
    // Should show validation error
    await waitFor(() => {
      expect(screen.getByText(/Please enter a valid 6-digit account number/)).toBeInTheDocument()
    })
    
    // Should still be on account input page
    expect(screen.getByText('Enter Account Number')).toBeInTheDocument()
  })
})
