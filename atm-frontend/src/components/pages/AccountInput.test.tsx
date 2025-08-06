// AccountInput component tests
// Run these tests with: npm test AccountInput.test.tsx

import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { AccountInput } from './AccountInput'
import { ATMProvider, ErrorProvider, LoadingProvider } from '../../context'

// Test wrapper with all required providers
const TestWrapper = ({ children }: { children: React.ReactNode }) => (
  <ErrorProvider>
    <LoadingProvider>
      <ATMProvider>
        {children}
      </ATMProvider>
    </LoadingProvider>
  </ErrorProvider>
)

describe('AccountInput Component', () => {
  const mockOnAccountSubmit = vi.fn()

  beforeEach(() => {
    mockOnAccountSubmit.mockClear()
  })

  test('renders account input form', () => {
    render(
      <TestWrapper>
        <AccountInput onAccountSubmit={mockOnAccountSubmit} />
      </TestWrapper>
    )
    
    expect(screen.getByText('Enter Account Number')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('123456')).toBeInTheDocument()
    expect(screen.getByText('Continue')).toBeInTheDocument()
  })

  test('shows demo account numbers', () => {
    render(
      <TestWrapper>
        <AccountInput onAccountSubmit={mockOnAccountSubmit} />
      </TestWrapper>
    )
    
    expect(screen.getByText('Demo Account Numbers:')).toBeInTheDocument()
    expect(screen.getByText(/123456 - Standard Account/)).toBeInTheDocument()
    expect(screen.getByText(/654321 - Premium Account/)).toBeInTheDocument()
    expect(screen.getByText(/111111 - Low Balance Account/)).toBeInTheDocument()
  })

  test('validates account number format', async () => {
    render(
      <TestWrapper>
        <AccountInput onAccountSubmit={mockOnAccountSubmit} />
      </TestWrapper>
    )
    
    const input = screen.getByPlaceholderText('123456')
    const submitButton = screen.getByText('Continue')
    
    // Try to submit with empty input
    fireEvent.click(submitButton)
    await waitFor(() => {
      expect(screen.getByText(/Please enter a valid 6-digit account number/)).toBeInTheDocument()
    })
    
    // Try with invalid format
    fireEvent.change(input, { target: { value: 'abc123' } })
    fireEvent.click(submitButton)
    await waitFor(() => {
      expect(screen.getByText(/Account number must contain only digits/)).toBeInTheDocument()
    })
  })

  test('only allows numeric input', () => {
    render(
      <TestWrapper>
        <AccountInput onAccountSubmit={mockOnAccountSubmit} />
      </TestWrapper>
    )
    
    const input = screen.getByPlaceholderText('123456')
    
    fireEvent.change(input, { target: { value: 'abc123def' } })
    expect(input).toHaveValue('123')
  })

  test('limits input to 6 digits', () => {
    render(
      <TestWrapper>
        <AccountInput onAccountSubmit={mockOnAccountSubmit} />
      </TestWrapper>
    )
    
    const input = screen.getByPlaceholderText('123456')
    
    fireEvent.change(input, { target: { value: '1234567890' } })
    expect(input).toHaveValue('123456')
  })

  test('enables continue button only with 6 digits', () => {
    render(
      <TestWrapper>
        <AccountInput onAccountSubmit={mockOnAccountSubmit} />
      </TestWrapper>
    )
    
    const input = screen.getByPlaceholderText('123456')
    const submitButton = screen.getByText('Continue')
    
    // Initially disabled
    expect(submitButton).toBeDisabled()
    
    // Still disabled with less than 6 digits
    fireEvent.change(input, { target: { value: '12345' } })
    expect(submitButton).toBeDisabled()
    
    // Enabled with exactly 6 digits
    fireEvent.change(input, { target: { value: '123456' } })
    expect(submitButton).not.toBeDisabled()
  })

  test('calls onAccountSubmit with valid account number', async () => {
    render(
      <TestWrapper>
        <AccountInput onAccountSubmit={mockOnAccountSubmit} />
      </TestWrapper>
    )
    
    const input = screen.getByPlaceholderText('123456')
    const submitButton = screen.getByText('Continue')
    
    fireEvent.change(input, { target: { value: '123456' } })
    fireEvent.click(submitButton)
    
    await waitFor(() => {
      expect(mockOnAccountSubmit).toHaveBeenCalledWith('123456')
    })
  })

  test('clears errors when user starts typing', async () => {
    render(
      <TestWrapper>
        <AccountInput onAccountSubmit={mockOnAccountSubmit} />
      </TestWrapper>
    )
    
    const input = screen.getByPlaceholderText('123456')
    const submitButton = screen.getByText('Continue')
    
    // Trigger an error first
    fireEvent.click(submitButton)
    await waitFor(() => {
      expect(screen.getByText(/Please enter a valid 6-digit account number/)).toBeInTheDocument()
    })
    
    // Start typing to clear error
    fireEvent.change(input, { target: { value: '1' } })
    await waitFor(() => {
      expect(screen.queryByText(/Please enter a valid 6-digit account number/)).not.toBeInTheDocument()
    })
  })
})
