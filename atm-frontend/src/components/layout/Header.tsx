import React from 'react';
import { useATM } from '../../context';

const Header: React.FC = () => {
  const { state } = useATM();
  const { account, isConnected } = state;

  return (
    <header className="bg-primary-600 text-white shadow-lg">
      <div className="max-w-4xl mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center">
              <svg
                className="w-5 h-5 text-primary-600"
                fill="currentColor"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path d="M2 10h20v2H2v-2zm0 4h20v2H2v-2zm0-8h20v2H2V6z" />
                <path d="M4 2h16c1.1 0 2 .9 2 2v16c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2zm0 2v16h16V4H4z" />
              </svg>
            </div>
            <div>
              <h1 className="text-xl font-bold">ATM System</h1>
              <p className="text-primary-200 text-sm">Secure Banking Operations</p>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            {/* Connection Status */}
            <div className="flex items-center gap-2">
              <div
                className={`w-3 h-3 rounded-full ${
                  isConnected ? 'bg-success-400' : 'bg-error-400'
                }`}
              />
              <span className="text-sm">
                {isConnected ? 'Connected' : 'Offline'}
              </span>
            </div>
            
            {/* Current Account */}
            {account.currentAccount && (
              <div className="text-right">
                <p className="text-sm text-primary-200">Account</p>
                <p className="font-mono font-semibold">
                  {account.currentAccount}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
