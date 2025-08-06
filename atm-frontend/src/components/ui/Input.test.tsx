// Input component tests
// Run these tests with: npm test Input.test.tsx

import { render, screen, fireEvent } from '@testing-library/react'
import Input from './Input'

describe('Input Component', () => {
  test('renders input with placeholder', () => {
    render(<Input value="" onChange={() => {}} placeholder="Enter text" />)
    expect(screen.getByPlaceholderText('Enter text')).toBeInTheDocument()
  })

  test('calls onChange when value changes', () => {
    const handleChange = vi.fn()
    render(<Input value="" onChange={handleChange} />)
    
    const input = screen.getByRole('textbox')
    fireEvent.change(input, { target: { value: 'test' } })
    
    expect(handleChange).toHaveBeenCalledWith('test')
  })

  test('displays current value', () => {
    render(<Input value="current value" onChange={() => {}} />)
    const input = screen.getByRole('textbox')
    expect(input).toHaveValue('current value')
  })

  test('renders label when provided', () => {
    render(<Input value="" onChange={() => {}} label="Account Number" id="account" />)
    expect(screen.getByLabelText('Account Number')).toBeInTheDocument()
  })

  test('shows required indicator when required', () => {
    render(<Input value="" onChange={() => {}} label="Required Field" required id="req" />)
    expect(screen.getByText('*')).toBeInTheDocument()
  })

  test('displays error message when error prop is provided', () => {
    render(<Input value="" onChange={() => {}} error="This field is required" />)
    expect(screen.getByText('This field is required')).toBeInTheDocument()
  })

  test('applies error styling when error is present', () => {
    render(<Input value="" onChange={() => {}} error="Error message" />)
    const input = screen.getByRole('textbox')
    expect(input).toHaveClass('border-error-500')
  })

  test('is disabled when disabled prop is true', () => {
    render(<Input value="" onChange={() => {}} disabled />)
    const input = screen.getByRole('textbox')
    expect(input).toBeDisabled()
  })

  test('respects maxLength prop', () => {
    render(<Input value="" onChange={() => {}} maxLength={6} />)
    const input = screen.getByRole('textbox')
    expect(input).toHaveAttribute('maxLength', '6')
  })

  test('supports different input types', () => {
    render(<Input value="" onChange={() => {}} type="tel" />)
    const input = screen.getByRole('textbox')
    expect(input).toHaveAttribute('type', 'tel')
  })
})
