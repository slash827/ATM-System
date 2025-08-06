# ATM System Frontend

A modern React/TypeScript frontend for the ATM System API, built with Vite and styled with Tailwind CSS.

## 🏗️ Technology Stack

- **React 18.3.1** - Modern React with hooks and concurrent features
- **TypeScript 5.6.3** - Type safety and enhanced developer experience
- **Vite 5.4.9** - Fast build tool and development server
- **Tailwind CSS 3.4.17** - Utility-first CSS framework for responsive design
- **ESLint** - Code linting and quality assurance

## 🚀 Features

### Core Banking Interface
- **Account Dashboard** - Comprehensive overview with balance display and quick actions
- **Balance Inquiry** - Real-time account balance checking
- **Cash Withdrawal** - Secure withdrawal interface with validation
- **Cash Deposit** - Simple deposit interface with confirmation
- **Money Transfer** - Transfer funds between accounts
- **Time Deposits** - Create and manage fixed-term deposits

### User Experience
- **Responsive Design** - Mobile-first approach with Tailwind CSS
- **Real-time Updates** - Live balance updates after transactions
- **Error Handling** - User-friendly error messages and validation
- **Loading States** - Visual feedback during API calls
- **Type Safety** - Full TypeScript implementation

## 🛠️ Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn package manager

### Installation

1. **Navigate to frontend directory**
```bash
cd atm-frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start development server**
```bash
npm run dev
```

4. **Access the application**
- Frontend: http://localhost:5173
- Backend API (required): http://localhost:8000

### Available Scripts

```bash
# Start development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm run test

# Run tests with coverage
npm run test:coverage

# Lint code
npm run lint

# Type checking
npm run type-check
```

## 📁 Project Structure

```
atm-frontend/
├── src/
│   ├── components/          # React components
│   │   ├── pages/          # Page components
│   │   │   ├── Dashboard.tsx    # Main dashboard
│   │   │   ├── BalanceCheck.tsx # Balance inquiry
│   │   │   ├── Withdraw.tsx     # Withdrawal interface
│   │   │   ├── Deposit.tsx      # Deposit interface
│   │   │   ├── MoneyTransfer.tsx # Transfer interface
│   │   │   └── TimeDeposits.tsx # Time deposit management
│   │   └── ui/             # Reusable UI components
│   │       ├── Button.tsx       # Button component
│   │       ├── Card.tsx         # Card layout component
│   │       └── Input.tsx        # Input field component
│   ├── context/            # React context providers
│   │   ├── ErrorContext.tsx     # Error state management
│   │   └── LoadingContext.tsx   # Loading state management
│   ├── services/           # API service layer
│   │   └── accounts.ts          # Account API calls
│   ├── types/              # TypeScript type definitions
│   │   └── index.ts             # Common types
│   ├── test/               # Test utilities
│   │   ├── testUtils.ts         # Testing helpers
│   │   └── vitest.d.ts          # Vitest type definitions
│   ├── App.tsx             # Main application component
│   ├── main.tsx            # Application entry point
│   └── index.css           # Global styles and Tailwind
├── public/                 # Static assets
├── package.json            # Dependencies and scripts
├── vite.config.ts          # Vite configuration
├── tailwind.config.js      # Tailwind CSS configuration
├── tsconfig.json           # TypeScript configuration
└── README.md               # This file
```

## 🧪 Testing

The frontend includes comprehensive testing setup:

### Test Framework
- **Vitest** - Fast unit test runner
- **React Testing Library** - Component testing utilities
- **jsdom** - DOM simulation for testing

### Running Tests
```bash
# Run all tests
npm run test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage report
npm run test:coverage

# Run specific test file
npm run test -- Dashboard.test.tsx
```

### Test Structure
```
src/
├── components/
│   └── ui/
│       └── Input.test.tsx   # Component tests
├── test/
│   ├── testUtils.ts         # Testing utilities
│   └── vitest.d.ts          # Type definitions
└── App.test.tsx             # Application tests
```

## 🎨 UI Components

### Reusable Components
- **Button** - Styled button with variants (primary, secondary, outline)
- **Card** - Layout component for content sections
- **Input** - Form input with validation styling
- **AccountInput** - Specialized account number input

### Design System
- **Colors** - Primary, secondary, success, error color schemes
- **Typography** - Consistent font sizes and weights
- **Spacing** - Tailwind spacing scale for consistency
- **Responsive** - Mobile-first breakpoints

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the frontend directory:
```
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_TITLE=ATM System
```

### Tailwind Configuration
The project uses a custom Tailwind configuration with:
- Custom color palette for banking interface
- Extended spacing and sizing utilities
- Responsive breakpoints for mobile/desktop

### TypeScript Configuration
- **Strict mode** enabled for maximum type safety
- **Path mapping** for clean imports
- **JSX** configured for React 18

## 🚀 Deployment

### Production Build
```bash
# Create optimized production build
npm run build

# Preview the production build
npm run preview
```

### Build Output
- **dist/** - Production-ready static files
- **Optimized assets** - Minified CSS and JavaScript
- **Source maps** - For debugging in production

### Deployment Platforms
- **Vercel** - Zero-config deployment for React apps
- **Netlify** - Static site hosting with CI/CD
- **Firebase Hosting** - Google's hosting platform
- **AWS S3** - Static website hosting
- **Railway** - Full-stack deployment platform

## 🔗 API Integration

### Backend Requirements
The frontend requires the ATM System backend API running on:
- **URL**: http://localhost:8000 (development)
- **Endpoints**: 
  - `GET /accounts/{account}/balance`
  - `POST /accounts/{account}/withdraw`
  - `POST /accounts/{account}/deposit`
  - `POST /accounts/{account}/transfer`

### Service Layer
API calls are handled through the `services/accounts.ts` module:
- Centralized API configuration
- Error handling and retry logic
- Type-safe request/response handling
- Currency formatting utilities

## 📚 Development Guidelines

### Code Style
- **ESLint** configuration for consistent code style
- **Prettier** formatting (recommended)
- **TypeScript strict mode** for type safety
- **Component naming** - PascalCase for components
- **File naming** - PascalCase for component files

### Best Practices
- **Component composition** over inheritance
- **Custom hooks** for reusable logic
- **Context providers** for state management
- **Error boundaries** for error handling
- **Accessibility** considerations (ARIA labels, keyboard navigation)

## 🤝 Contributing

1. Follow the existing code style and patterns
2. Add tests for new components and features
3. Update documentation for any API changes
4. Ensure TypeScript compilation passes
5. Test responsive design on multiple screen sizes

## 📋 TODO

### Immediate Tasks
- [ ] Complete test coverage for all components
- [ ] Add accessibility improvements (ARIA labels)
- [ ] Implement loading skeletons for better UX
- [ ] Add form validation with real-time feedback

### Future Enhancements
- [ ] Dark mode support
- [ ] Internationalization (i18n)
- [ ] Progressive Web App (PWA) features
- [ ] Advanced transaction history interface
- [ ] Biometric authentication integration

---

**Built with React + TypeScript + Vite**
