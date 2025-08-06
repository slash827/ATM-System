import React, { useState } from 'react';
import { transferMoney } from '../services/accounts';
import type { TransferRequest, TransferResponse } from '../types';

interface MoneyTransferProps {
  currentAccount: string;
  onTransferComplete?: (response: TransferResponse) => void;
  onBack?: () => void;
}

interface FormData {
  amount: string;
  recipientAccount: string;
  message: string;
}

interface FormErrors {
  amount?: string;
  recipientAccount?: string;
  message?: string;
}

const MoneyTransfer: React.FC<MoneyTransferProps> = ({
  currentAccount,
  onTransferComplete,
  onBack
}) => {
  const [formData, setFormData] = useState<FormData>({
    amount: '',
    recipientAccount: '',
    message: ''
  });
  
  const [errors, setErrors] = useState<FormErrors>({});
  const [isLoading, setIsLoading] = useState(false);
  const [showConfirmation, setShowConfirmation] = useState(false);

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    // Validate amount
    const amount = parseFloat(formData.amount);
    if (!formData.amount || isNaN(amount)) {
      newErrors.amount = 'Please enter a valid amount';
    } else if (amount <= 0) {
      newErrors.amount = 'Amount must be greater than zero';
    } else if (amount > 10000) {
      newErrors.amount = 'Transfer amount cannot exceed $10,000';
    } else if (!/^\d+(\.\d{1,2})?$/.test(formData.amount)) {
      newErrors.amount = 'Amount must have at most 2 decimal places';
    }

    // Validate recipient account
    if (!formData.recipientAccount) {
      newErrors.recipientAccount = 'Please enter recipient account number';
    } else if (!/^\d{6}$/.test(formData.recipientAccount)) {
      newErrors.recipientAccount = 'Account number must be exactly 6 digits';
    } else if (formData.recipientAccount === currentAccount) {
      newErrors.recipientAccount = 'Cannot transfer to the same account';
    }

    // Validate message (optional but if provided, check length)
    if (formData.message && formData.message.length > 100) {
      newErrors.message = 'Message cannot exceed 100 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleInputChange = (field: keyof FormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    
    // Clear error for this field when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (validateForm()) {
      setShowConfirmation(true);
    }
  };

  const executeTransfer = async () => {
    if (!validateForm()) return;

    setIsLoading(true);
    
    try {
      const transferRequest: TransferRequest = {
        amount: parseFloat(formData.amount),
        recipient_account: formData.recipientAccount,
        message: formData.message || undefined
      };

      const response = await transferMoney(currentAccount, transferRequest);
      
      // Successfully executed transfer
      onTransferComplete?.(response.data);
    } catch (error) {
      console.error('Transfer error:', error);
      setErrors({ amount: 'Transfer failed. Please try again.' });
    } finally {
      setIsLoading(false);
      setShowConfirmation(false);
    }
  };

  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(amount);
  };

  if (showConfirmation) {
    return (
      <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
          Confirm Transfer
        </h2>
        
        <div className="space-y-4 mb-6">
          <div className="border-b pb-4">
            <p className="text-sm text-gray-600">From Account</p>
            <p className="text-lg font-semibold text-gray-800">{currentAccount}</p>
          </div>
          
          <div className="border-b pb-4">
            <p className="text-sm text-gray-600">To Account</p>
            <p className="text-lg font-semibold text-gray-800">{formData.recipientAccount}</p>
          </div>
          
          <div className="border-b pb-4">
            <p className="text-sm text-gray-600">Amount</p>
            <p className="text-lg font-semibold text-green-600">
              {formatCurrency(parseFloat(formData.amount))}
            </p>
          </div>
          
          {formData.message && (
            <div className="border-b pb-4">
              <p className="text-sm text-gray-600">Message</p>
              <p className="text-gray-800">{formData.message}</p>
            </div>
          )}
        </div>

        <div className="flex space-x-3">
          <button
            onClick={() => setShowConfirmation(false)}
            className="flex-1 bg-gray-500 text-white py-3 px-4 rounded-lg hover:bg-gray-600 transition duration-200"
            disabled={isLoading}
          >
            Cancel
          </button>
          <button
            onClick={executeTransfer}
            disabled={isLoading}
            className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition duration-200 disabled:opacity-50"
          >
            {isLoading ? 'Processing...' : 'Confirm Transfer'}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Transfer Money</h2>
        {onBack && (
          <button
            onClick={onBack}
            className="text-gray-500 hover:text-gray-700 transition duration-200"
            aria-label="Go back"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
        )}
      </div>

      <div className="mb-4 p-3 bg-gray-50 rounded-lg">
        <p className="text-sm text-gray-600">From Account</p>
        <p className="text-lg font-semibold text-gray-800">{currentAccount}</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="recipientAccount" className="block text-sm font-medium text-gray-700 mb-1">
            Recipient Account Number
          </label>
          <input
            type="text"
            id="recipientAccount"
            value={formData.recipientAccount}
            onChange={(e) => handleInputChange('recipientAccount', e.target.value)}
            placeholder="Enter 6-digit account number"
            className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              errors.recipientAccount ? 'border-red-500' : 'border-gray-300'
            }`}
            maxLength={6}
          />
          {errors.recipientAccount && (
            <p className="text-red-500 text-sm mt-1">{errors.recipientAccount}</p>
          )}
        </div>

        <div>
          <label htmlFor="amount" className="block text-sm font-medium text-gray-700 mb-1">
            Amount
          </label>
          <div className="relative">
            <span className="absolute left-3 top-2 text-gray-500">$</span>
            <input
              type="number"
              id="amount"
              step="0.01"
              min="0"
              max="10000"
              value={formData.amount}
              onChange={(e) => handleInputChange('amount', e.target.value)}
              placeholder="0.00"
              className={`w-full pl-8 pr-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.amount ? 'border-red-500' : 'border-gray-300'
              }`}
            />
          </div>
          {errors.amount && (
            <p className="text-red-500 text-sm mt-1">{errors.amount}</p>
          )}
        </div>

        <div>
          <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-1">
            Message (Optional)
          </label>
          <textarea
            id="message"
            value={formData.message}
            onChange={(e) => handleInputChange('message', e.target.value)}
            placeholder="Add a note for this transfer"
            rows={3}
            maxLength={100}
            className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none ${
              errors.message ? 'border-red-500' : 'border-gray-300'
            }`}
          />
          <div className="flex justify-between items-center mt-1">
            {errors.message && (
              <p className="text-red-500 text-sm">{errors.message}</p>
            )}
            <p className="text-gray-400 text-xs ml-auto">
              {formData.message.length}/100
            </p>
          </div>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Review Transfer
        </button>
      </form>
    </div>
  );
};

export default MoneyTransfer;
