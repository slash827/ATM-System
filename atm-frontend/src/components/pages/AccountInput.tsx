import { useState } from 'react';
import { Card, Button, Input } from '../ui';
import { useATM } from '../../context/ATMContext';
import { useError } from '../../context/ErrorContext';
import { useLoading } from '../../context/LoadingContext';

interface AccountInputProps {
  onAccountSubmit: (accountNumber: string) => void;
}

export const AccountInput = ({ onAccountSubmit }: AccountInputProps) => {
  const [accountNumber, setAccountNumber] = useState('');
  const { setAccount } = useATM();
  const { setError, clearError } = useError();
  const { setGlobalLoading } = useLoading();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!accountNumber || accountNumber.length !== 6) {
      setError('Please enter a valid 6-digit account number');
      return;
    }

    if (!/^\d{6}$/.test(accountNumber)) {
      setError('Account number must contain only digits');
      return;
    }

    try {
      setGlobalLoading(true, 'Validating account...');
      clearError();
      
      // Set the account in context
      setAccount(accountNumber);
      
      // Call the parent handler
      onAccountSubmit(accountNumber);
    } catch (error) {
      setError('Failed to validate account number');
    } finally {
      setGlobalLoading(false);
    }
  };

  const handleInputChange = (value: string) => {
    const cleanValue = value.replace(/\D/g, '').slice(0, 6);
    setAccountNumber(cleanValue);
    
    // Clear any previous errors when user starts typing
    if (cleanValue.length > 0) {
      clearError();
    }
  };

  return (
    <div className="max-w-md mx-auto">
      <Card 
        title="Enter Account Number"
        description="Please enter your 6-digit account number to access your account."
      >
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="accountNumber" className="block text-sm font-medium text-gray-700 mb-2">
              Account Number *
            </label>
            <Input
              id="accountNumber"
              type="text"
              value={accountNumber}
              onChange={handleInputChange}
              placeholder="123456"
              maxLength={6}
              className="text-center text-lg tracking-widest"
            />
            <p className="text-sm text-gray-500 mt-2">
              Enter exactly 6 digits
            </p>
          </div>
          
          <Button 
            type="submit" 
            variant="primary" 
            size="lg"
            className="w-full"
            disabled={accountNumber.length !== 6}
          >
            Continue
          </Button>
        </form>
        
        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="text-sm text-gray-600">
            <p className="font-medium mb-2">Demo Account Numbers:</p>
            <div className="space-y-1">
              <p>• 123456 - Standard Account ($1,000.00)</p>
              <p>• 654321 - Premium Account ($5,000.00)</p>
              <p>• 111111 - Low Balance Account ($25.50)</p>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};
