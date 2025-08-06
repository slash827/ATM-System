import React, { useState, useEffect } from 'react';
import { Card, Button } from '../ui';
import { accountsService } from '../../services/accounts';
import { useError, useLoading } from '../../context';

interface DashboardProps {
  accountNumber: string;
  onNavigate: (page: 'balance' | 'withdraw' | 'deposit' | 'time-deposits') => void;
  onBackToHome: () => void;
}

const Dashboard: React.FC<DashboardProps> = ({ accountNumber, onNavigate, onBackToHome }) => {
  const [balance, setBalance] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const { setError } = useError();
  const { setGlobalLoading } = useLoading();

  // Automatically load balance when dashboard mounts
  useEffect(() => {
    const loadBalance = async () => {
      try {
        setGlobalLoading(true, 'Loading account information...');
        const response = await accountsService.getBalance(accountNumber);
        setBalance(response.data.balance);
      } catch (error: any) {
        setError(error.detail || 'Failed to load account information');
      } finally {
        setGlobalLoading(false);
        setIsLoading(false);
      }
    };

    loadBalance();
  }, [accountNumber, setError, setGlobalLoading]);

  const refreshBalance = async () => {
    try {
      setGlobalLoading(true, 'Refreshing balance...');
      const response = await accountsService.getBalance(accountNumber);
      setBalance(response.data.balance);
    } catch (error: any) {
      setError(error.detail || 'Failed to refresh balance');
    } finally {
      setGlobalLoading(false);
    }
  };

  if (isLoading) {
    return (
      <Card title="Loading Dashboard..." description="Please wait while we load your account information.">
        <div className="text-center py-8">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Account Overview */}
      <Card
        title={`Welcome, Account ${accountNumber}`}
        description="Your account dashboard - view balance and manage transactions"
      >
        {/* Current Balance Display */}
        <div className="bg-gradient-to-r from-primary-50 to-primary-100 border border-primary-200 rounded-lg p-6 mb-6">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="text-lg font-semibold text-primary-800 mb-1">
                Current Balance
              </h3>
              <div className="text-3xl font-bold text-primary-700 font-mono">
                {balance !== null ? accountsService.formatCurrency(balance) : 'Loading...'}
              </div>
              <p className="text-sm text-primary-600 mt-1">
                Account: {accountNumber}
              </p>
            </div>
            <Button 
              variant="outline" 
              size="sm"
              onClick={refreshBalance}
              className="ml-4"
            >
              Refresh
            </Button>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Button 
            variant="primary" 
            size="lg"
            onClick={() => onNavigate('balance')}
            className="flex flex-col items-center space-y-2 py-6"
          >
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
            <span>Check Balance</span>
          </Button>
          
          <Button 
            variant="primary" 
            size="lg"
            onClick={() => onNavigate('withdraw')}
            className="flex flex-col items-center space-y-2 py-6"
          >
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <span>Withdraw</span>
          </Button>
          
          <Button 
            variant="success" 
            size="lg"
            onClick={() => onNavigate('deposit')}
            className="flex flex-col items-center space-y-2 py-6"
          >
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            <span>Deposit</span>
          </Button>
          
          <Button 
            variant="secondary" 
            size="lg"
            onClick={() => onNavigate('time-deposits')}
            className="flex flex-col items-center space-y-2 py-6"
          >
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>Time Deposits</span>
          </Button>
        </div>
        
        {/* Account Summary */}
        <div className="mt-8 pt-6 border-t border-gray-200">
          <h4 className="text-md font-semibold text-gray-800 mb-4">Quick Account Summary</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-gray-600 font-medium">Available Balance</div>
              <div className="text-lg font-semibold text-gray-800 mt-1">
                {balance !== null ? accountsService.formatCurrency(balance) : '--'}
              </div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-gray-600 font-medium">Account Type</div>
              <div className="text-lg font-semibold text-gray-800 mt-1">Checking</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-gray-600 font-medium">Account Status</div>
              <div className="text-lg font-semibold text-green-600 mt-1">Active</div>
            </div>
          </div>
        </div>
        
        <div className="mt-6 pt-6 border-t border-gray-200">
          <Button 
            variant="outline" 
            onClick={onBackToHome}
          >
            Back to Home
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default Dashboard;
