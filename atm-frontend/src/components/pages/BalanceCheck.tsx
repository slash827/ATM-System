import React, { useState } from 'react';
import { Card, Button } from '../ui';
import { accountsService } from '../../services/accounts';
import { useError, useLoading } from '../../context';

interface BalanceCheckProps {
  accountNumber: string;
  onBack: () => void;
}

const BalanceCheck: React.FC<BalanceCheckProps> = ({ accountNumber, onBack }) => {
  const [balance, setBalance] = useState<number | null>(null);
  const [isChecked, setIsChecked] = useState(false);
  const { setError } = useError();
  const { setGlobalLoading } = useLoading();

  const handleCheckBalance = async () => {
    try {
      setGlobalLoading(true, 'Checking balance...');
      const response = await accountsService.getBalance(accountNumber);
      setBalance(response.data.balance);
      setIsChecked(true);
    } catch (error: any) {
      setError(error.detail || 'Failed to check balance');
    } finally {
      setGlobalLoading(false);
    }
  };

  const handleNewCheck = () => {
    setBalance(null);
    setIsChecked(false);
  };

  return (
    <div className="space-y-6">
      <Card
        title="Balance Inquiry"
        description={`Checking balance for account ${accountNumber}`}
      >
        {!isChecked ? (
          <div className="text-center space-y-4">
            <p className="text-gray-600">
              Click the button below to check your current account balance.
            </p>
            <Button 
              variant="primary" 
              size="lg"
              onClick={handleCheckBalance}
            >
              Check Balance
            </Button>
          </div>
        ) : (
          <div className="text-center space-y-6">
            <div className="bg-primary-50 border border-primary-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-primary-800 mb-2">
                Current Balance
              </h3>
              <div className="text-3xl font-bold text-primary-700 font-mono">
                {balance !== null ? accountsService.formatCurrency(balance) : 'Loading...'}
              </div>
              <p className="text-sm text-primary-600 mt-2">
                Account: {accountNumber}
              </p>
            </div>
            
            <div className="flex justify-center gap-3">
              <Button 
                variant="outline" 
                onClick={handleNewCheck}
              >
                Check Again
              </Button>
              <Button 
                variant="secondary" 
                onClick={onBack}
              >
                Back to Operations
              </Button>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
};

export default BalanceCheck;
