import React, { useState, useEffect } from 'react';
import { createTimeDeposit, listTimeDeposits, matureTimeDeposit } from '../services/accounts';
import type { CreateTimeDepositRequest, TimeDeposit, TimeDepositResponse } from '../types';

interface TimeDepositsProps {
  currentAccount: string;
  onDepositComplete?: (response: TimeDepositResponse) => void;
  onBack?: () => void;
}

interface FormData {
  amount: string;
  duration: string;
}

interface FormErrors {
  amount?: string;
  duration?: string;
}

const TimeDeposits: React.FC<TimeDepositsProps> = ({
  currentAccount,
  onDepositComplete,
  onBack
}) => {
  const [formData, setFormData] = useState<FormData>({
    amount: '',
    duration: ''
  });
  
  const [errors, setErrors] = useState<FormErrors>({});
  const [isLoading, setIsLoading] = useState(false);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [timeDeposits, setTimeDeposits] = useState<TimeDeposit[]>([]);
  const [isLoadingDeposits, setIsLoadingDeposits] = useState(false);

  // Interest rate information
  const getInterestRate = (months: number): number => {
    if (months >= 12) return 4.0;
    if (months >= 6) return 3.0;
    if (months >= 3) return 2.0;
    return 0.0;
  };

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    // Validate amount
    const amount = parseFloat(formData.amount);
    if (!formData.amount || isNaN(amount)) {
      newErrors.amount = 'Please enter a valid amount';
    } else if (amount < 100) {
      newErrors.amount = 'Minimum deposit amount is $100';
    } else if (amount > 50000) {
      newErrors.amount = 'Maximum deposit amount is $50,000';
    } else if (!/^\d+(\.\d{1,2})?$/.test(formData.amount)) {
      newErrors.amount = 'Amount must have at most 2 decimal places';
    }

    // Validate duration
    const duration = parseInt(formData.duration);
    if (!formData.duration || isNaN(duration)) {
      newErrors.duration = 'Please select a duration';
    } else if (duration < 3 || duration > 60) {
      newErrors.duration = 'Duration must be between 3 and 60 months';
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

  const handleCreateDeposit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setIsLoading(true);
    
    try {
      const depositRequest: CreateTimeDepositRequest = {
        amount: parseFloat(formData.amount),
        duration_months: parseInt(formData.duration)
      };

      const response = await createTimeDeposit(currentAccount, depositRequest);
      
      onDepositComplete?.(response.data);
      setShowCreateForm(false);
      setFormData({ amount: '', duration: '' });
      loadTimeDeposits(); // Refresh the list
    } catch (error) {
      console.error('Time deposit creation error:', error);
      setErrors({ amount: 'Failed to create time deposit. Please try again.' });
    } finally {
      setIsLoading(false);
    }
  };

  const loadTimeDeposits = async () => {
    setIsLoadingDeposits(true);
    try {
      const response = await listTimeDeposits(currentAccount);
      setTimeDeposits(response.data.deposits);
    } catch (error) {
      console.error('Failed to load time deposits:', error);
    } finally {
      setIsLoadingDeposits(false);
    }
  };

  const handleMatureDeposit = async (depositId: string) => {
    try {
      const response = await matureTimeDeposit(depositId);
      console.log('Deposit matured:', response.data);
      loadTimeDeposits(); // Refresh the list
    } catch (error) {
      console.error('Failed to mature deposit:', error);
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

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const isMatured = (maturityDate: string): boolean => {
    return new Date(maturityDate) <= new Date();
  };

  // Load time deposits on component mount
  useEffect(() => {
    loadTimeDeposits();
  }, [currentAccount]);

  if (showCreateForm) {
    return (
      <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-800">Create Time Deposit</h2>
          <button
            onClick={() => setShowCreateForm(false)}
            className="text-gray-500 hover:text-gray-700 transition duration-200"
            aria-label="Go back"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
        </div>

        <div className="mb-4 p-3 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600">Account Number</p>
          <p className="text-lg font-semibold text-gray-800">{currentAccount}</p>
        </div>

        <form onSubmit={handleCreateDeposit} className="space-y-4">
          <div>
            <label htmlFor="amount" className="block text-sm font-medium text-gray-700 mb-1">
              Deposit Amount
            </label>
            <div className="relative">
              <span className="absolute left-3 top-2 text-gray-500">$</span>
              <input
                type="number"
                id="amount"
                step="0.01"
                min="100"
                max="50000"
                value={formData.amount}
                onChange={(e) => handleInputChange('amount', e.target.value)}
                placeholder="100.00"
                className={`w-full pl-8 pr-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.amount ? 'border-red-500' : 'border-gray-300'
                }`}
              />
            </div>
            {errors.amount && (
              <p className="text-red-500 text-sm mt-1">{errors.amount}</p>
            )}
            <p className="text-xs text-gray-500 mt-1">Minimum: $100, Maximum: $50,000</p>
          </div>

          <div>
            <label htmlFor="duration" className="block text-sm font-medium text-gray-700 mb-1">
              Duration (Months)
            </label>
            <select
              id="duration"
              value={formData.duration}
              onChange={(e) => handleInputChange('duration', e.target.value)}
              className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.duration ? 'border-red-500' : 'border-gray-300'
              }`}
            >
              <option value="">Select duration</option>
              <option value="3">3 months (2% APY)</option>
              <option value="6">6 months (3% APY)</option>
              <option value="12">12 months (4% APY)</option>
              <option value="24">24 months (4% APY)</option>
            </select>
            {errors.duration && (
              <p className="text-red-500 text-sm mt-1">{errors.duration}</p>
            )}
          </div>

          {formData.amount && formData.duration && (
            <div className="bg-blue-50 p-4 rounded-lg">
              <h3 className="font-semibold text-blue-800 mb-2">Projected Earnings</h3>
              <div className="text-sm text-blue-700">
                <p>Principal: {formatCurrency(parseFloat(formData.amount) || 0)}</p>
                <p>Interest Rate: {getInterestRate(parseInt(formData.duration) || 0)}% APY</p>
                <p>Duration: {formData.duration} months</p>
                <p className="font-semibold mt-2">
                  Estimated Total at Maturity: {formatCurrency(
                    (parseFloat(formData.amount) || 0) * 
                    (1 + getInterestRate(parseInt(formData.duration) || 0) / 100 * 
                    (parseInt(formData.duration) || 0) / 12)
                  )}
                </p>
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-green-600 text-white py-3 px-4 rounded-lg hover:bg-green-700 transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Creating Deposit...' : 'Create Time Deposit'}
          </button>
        </form>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Time Deposits</h2>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowCreateForm(true)}
            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition duration-200"
          >
            Create New Deposit
          </button>
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
      </div>

      <div className="mb-4 p-3 bg-gray-50 rounded-lg">
        <p className="text-sm text-gray-600">Account Number</p>
        <p className="text-lg font-semibold text-gray-800">{currentAccount}</p>
      </div>

      <div className="mb-6 bg-blue-50 p-4 rounded-lg">
        <h3 className="font-semibold text-blue-800 mb-2">Interest Rates</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-blue-700">
          <div>
            <p className="font-medium">3-5 months</p>
            <p>2.0% APY</p>
          </div>
          <div>
            <p className="font-medium">6-11 months</p>
            <p>3.0% APY</p>
          </div>
          <div>
            <p className="font-medium">12+ months</p>
            <p>4.0% APY</p>
          </div>
        </div>
      </div>

      {isLoadingDeposits ? (
        <div className="text-center py-8">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-2 text-gray-600">Loading time deposits...</p>
        </div>
      ) : timeDeposits.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-gray-600">No time deposits found for this account.</p>
          <button
            onClick={() => setShowCreateForm(true)}
            className="mt-4 bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition duration-200"
          >
            Create Your First Time Deposit
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {timeDeposits.map((deposit) => (
            <div
              key={deposit.deposit_id}
              className={`border rounded-lg p-4 ${
                isMatured(deposit.maturity_date) ? 'border-green-300 bg-green-50' : 'border-gray-300'
              }`}
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div>
                      <p className="text-sm text-gray-600">Principal Amount</p>
                      <p className="font-semibold text-green-600">{formatCurrency(deposit.amount)}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Interest Rate</p>
                      <p className="font-semibold">{deposit.interest_rate}% APY</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Created</p>
                      <p className="font-medium">{formatDate(deposit.created_at)}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Maturity Date</p>
                      <p className="font-medium">{formatDate(deposit.maturity_date)}</p>
                    </div>
                  </div>
                  <div className="mt-3 grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-600">Duration</p>
                      <p className="font-medium">{deposit.duration_months} months</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Status</p>
                      <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${
                        isMatured(deposit.maturity_date) 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {isMatured(deposit.maturity_date) ? 'Matured' : 'Active'}
                      </span>
                    </div>
                  </div>
                </div>
                {isMatured(deposit.maturity_date) && (
                  <button
                    onClick={() => handleMatureDeposit(deposit.deposit_id)}
                    className="ml-4 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition duration-200"
                  >
                    Withdraw
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TimeDeposits;
