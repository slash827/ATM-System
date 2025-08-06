import { useState } from 'react';
import { ATMProvider, ErrorProvider, LoadingProvider } from './context';
import { Layout } from './components/layout';
import { Card, Button } from './components/ui';
import { AccountInput } from './components/pages/AccountInput';
import BalanceCheck from './components/pages/BalanceCheck';
import Withdraw from './components/pages/Withdraw';
import Deposit from './components/pages/Deposit';
import Dashboard from './components/pages/Dashboard';
import TimeDeposits from './components/pages/TimeDeposits';

type AppPage = 'home' | 'account-input' | 'dashboard' | 'balance' | 'withdraw' | 'deposit' | 'time-deposits';

function App() {
  const [currentPage, setCurrentPage] = useState<AppPage>('home');
  const [currentAccount, setCurrentAccount] = useState<string | null>(null);

  const handleGetStarted = () => {
    setCurrentPage('account-input');
  };

  const handleAccountSubmit = (accountNumber: string) => {
    setCurrentAccount(accountNumber);
    setCurrentPage('dashboard');
  };

  const handleBackToHome = () => {
    setCurrentAccount(null);
    setCurrentPage('home');
  };

  const handleBackToDashboard = () => {
    setCurrentPage('dashboard');
  };

  const handleNavigateFromDashboard = (page: 'balance' | 'withdraw' | 'deposit' | 'time-deposits') => {
    setCurrentPage(page);
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return (
          <div className="space-y-8">
            {/* Welcome Section */}
            <Card
              title="Welcome to ATM System"
              description="Your secure banking solution for all your financial needs."
            >
              <div className="space-y-6 mt-6">
                <div className="text-center">
                  <h3 className="text-lg font-semibold text-gray-800 mb-2">
                    Available Services
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="text-center p-4 bg-primary-50 rounded-lg">
                      <div className="text-primary-600 font-medium">Balance Inquiry</div>
                      <div className="text-sm text-gray-600 mt-1">Check your account balance</div>
                    </div>
                    <div className="text-center p-4 bg-success-50 rounded-lg">
                      <div className="text-success-600 font-medium">Cash Withdrawal</div>
                      <div className="text-sm text-gray-600 mt-1">Withdraw money safely</div>
                    </div>
                    <div className="text-center p-4 bg-warning-50 rounded-lg">
                      <div className="text-warning-600 font-medium">Deposit Funds</div>
                      <div className="text-sm text-gray-600 mt-1">Deposit cash or checks</div>
                    </div>
                  </div>
                </div>
                
                <div className="text-center">
                  <Button 
                    variant="primary" 
                    size="lg"
                    onClick={handleGetStarted}
                  >
                    Get Started
                  </Button>
                </div>
              </div>
            </Card>
            
            {/* Demo Status */}
            <Card>
              <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
                <div className="flex items-center">
                  <svg
                    className="w-5 h-5 text-primary-600 mr-2"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fillRule="evenodd"
                      d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                      clipRule="evenodd"
                    />
                  </svg>
                  <div>
                    <h3 className="text-sm font-medium text-primary-800">
                      Demo Mode Active
                    </h3>
                    <p className="text-sm text-primary-700 mt-1">
                      Frontend successfully connected to FastAPI backend. Ready for banking operations!
                    </p>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        );

      case 'account-input':
        return <AccountInput onAccountSubmit={handleAccountSubmit} />;

      case 'dashboard':
        return currentAccount ? (
          <Dashboard 
            accountNumber={currentAccount}
            onNavigate={handleNavigateFromDashboard}
            onBackToHome={handleBackToHome}
          />
        ) : null;

      case 'balance':
        return currentAccount ? (
          <BalanceCheck 
            accountNumber={currentAccount} 
            onBack={handleBackToDashboard} 
          />
        ) : null;

      case 'withdraw':
        return currentAccount ? (
          <Withdraw 
            accountNumber={currentAccount} 
            onBack={handleBackToDashboard} 
          />
        ) : null;

      case 'deposit':
        return currentAccount ? (
          <Deposit 
            accountNumber={currentAccount} 
            onBack={handleBackToDashboard} 
          />
        ) : null;

      case 'time-deposits':
        return currentAccount ? (
          <TimeDeposits 
            accountNumber={currentAccount} 
            onBack={handleBackToDashboard} 
          />
        ) : null;

      default:
        return null;
    }
  };

  return (
    <ErrorProvider>
      <LoadingProvider>
        <ATMProvider>
          <Layout>
            {renderPage()}
          </Layout>
        </ATMProvider>
      </LoadingProvider>
    </ErrorProvider>
  );
}

export default App;
