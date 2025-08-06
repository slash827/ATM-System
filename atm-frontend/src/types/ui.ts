// UI State types
export interface LoadingState {
  isLoading: boolean;
  operation?: string;
  progress?: number;
}

// Modal state
export interface ModalState {
  isOpen: boolean;
  type?: ModalType;
  data?: any;
}

export type ModalType = 'confirmation' | 'error' | 'success' | 'info';

// Navigation state
export interface NavigationState {
  currentPage: PageType;
  previousPage?: PageType;
  history: PageType[];
}

export type PageType = 'home' | 'balance' | 'withdraw' | 'deposit' | 'confirmation';

// Button variants and states
export type ButtonVariant = 'primary' | 'secondary' | 'success' | 'error' | 'outline';
export type ButtonSize = 'sm' | 'md' | 'lg' | 'xl';

export interface ButtonProps {
  variant?: ButtonVariant;
  size?: ButtonSize;
  disabled?: boolean;
  loading?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  className?: string;
}

// Input component props
export interface InputProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  type?: 'text' | 'number' | 'tel';
  maxLength?: number;
  disabled?: boolean;
  error?: string;
  className?: string;
  autoFocus?: boolean;
  id?: string;
  label?: string;
  required?: boolean;
}

// Card component props
export interface CardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  description?: string;
}

// Notification types
export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message?: string;
  duration?: number;
  timestamp: Date;
}

// Toast state
export interface ToastState {
  notifications: Notification[];
}
