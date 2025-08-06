# ATM Frontend Testing Guide

## 🧪 Testing Setup

### Install Testing Dependencies
```bash
cd atm-frontend
npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event vitest jsdom
```

### Run Tests
```bash
# Run all tests once
npm test

# Run tests in watch mode (reruns on file changes)
npm run test:watch

# Run tests with coverage report
npm run test:coverage

# Run tests with UI interface
npm run test:ui
```

## 📋 Test Coverage

### ✅ Component Tests Created
- **Button Component** (9 tests)
  - Rendering with different variants (primary, secondary, success, error, outline)
  - Click handling and disabled states
  - Size variations (sm, md, lg, xl)
  - Custom className support
  - Form submission types

- **Input Component** (10 tests)
  - Basic rendering with placeholder and value
  - Change event handling
  - Label and required field support
  - Error state display and styling
  - Disabled state
  - MaxLength validation
  - Different input types (text, tel, number)

- **AccountInput Component** (8 tests)
  - Form rendering and demo accounts display
  - Account number validation (6-digit requirement)
  - Numeric-only input filtering
  - Continue button enable/disable logic
  - Form submission with valid data
  - Error handling and clearing
  - Real-time validation feedback

- **App Integration Tests** (6 tests)
  - Home page rendering and content
  - Navigation between pages
  - Complete user flow testing
  - Back navigation functionality
  - Form validation integration
  - Demo mode status display

### 🎯 Test Scenarios Covered
1. **User Interface Testing**
   - Component rendering
   - Interactive elements
   - Form validation
   - Error states
   - Loading states

2. **User Journey Testing**
   - Home → Account Input → Operations flow
   - Navigation and back buttons
   - Input validation and error handling
   - Demo account number examples

3. **Integration Testing**
   - Context providers working together
   - State management across components
   - Error and loading context integration

## 🔧 Mock Data Available
- Valid/invalid account numbers
- Transaction responses
- API response mocking
- Error scenarios

## 📝 Test Commands Quick Reference
```bash
# Install and run tests
npm install
npm test

# Development with tests
npm run dev          # Start development server
npm run test:watch   # Run tests in watch mode (new terminal)
```

---

**Next Steps**: Once testing dependencies are installed, you can run the full test suite to verify all components work correctly before testing the live application.
