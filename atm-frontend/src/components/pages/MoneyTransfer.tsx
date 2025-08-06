import React, { useState } from 'react';
import { Card, Button, Input } from '../ui';
import { transferMoney } from '../../services/accounts';
import type { TransferResponse } from '../../types';

interface MoneyTransferProps {
  accountNumber: string;
  onBack: () => void;
}

const MoneyTransfer: React.FC<MoneyTransferProps> = ({ accountNumber, onBack }) => {
  const [amount, setAmount] = useState('');
  const [recipientAccount, setRecipientAccount] = useState('');
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [transferData, setTransferData] = useState<TransferResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleTransfer = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setTransferData(null);

    try {
      const numericAmount = parseFloat(amount);
      if (isNaN(numericAmount) || numericAmount <= 0) {
        throw new Error('Please enter a valid amount');
      }

      if (!recipientAccount.match(/^\d{6}$/)) {
        throw new Error('Recipient account must be exactly 6 digits');
      }

      if (recipientAccount === accountNumber) {
        throw new Error('Cannot transfer to the same account');
      }

      const response = await transferMoney(accountNumber, {
        amount: numericAmount,
        recipient_account: recipientAccount,
        message: message || undefined
      });
      
      setTransferData(response.data);
      setAmount('');
      setRecipientAccount('');
      setMessage('');
    } catch (err: any) {
      setError(err.message || 'Transfer failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <div className="p-6">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Money Transfer</h2>
          <p className="text-gray-600">Transfer money from account {accountNumber}</p>
        </div>

        {transferData && (
          <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
            <div className="text-green-800">
              <p className="font-medium mb-2">{transferData.message}</p>
              <div className="text-sm space-y-1">
                <p>From: {transferData.sender_account}</p>
                <p>To: {transferData.recipient_account}</p>
                <p>Amount: {formatCurrency(transferData.transfer_amount)}</p>
                <p>Previous Balance: {formatCurrency(transferData.sender_previous_balance)}</p>
                <p>New Balance: {formatCurrency(transferData.sender_new_balance)}</p>
                {transferData.transfer_message && (
                  <p>Message: "{transferData.transfer_message}"</p>
                )}
                <p className="text-xs text-green-600">
                  Time: {new Date(transferData.timestamp).toLocaleString()}
                </p>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        <form onSubmit={handleTransfer} className="space-y-4">
          <div>
            <label htmlFor="recipient" className="block text-sm font-medium text-gray-700 mb-2">
              Recipient Account Number
            </label>
            <Input
              id="recipient"
              type="text"
              value={recipientAccount}
              onChange={(value) => setRecipientAccount(value)}
              placeholder="123456"
              maxLength={6}
              required
              className="w-full"
            />
            <p className="text-xs text-gray-500 mt-1">
              Enter the 6-digit account number
            </p>
          </div>

          <div>
            <label htmlFor="amount" className="block text-sm font-medium text-gray-700 mb-2">
              Transfer Amount
            </label>
            <Input
              id="amount"
              type="number"
              value={amount}
              onChange={(value) => setAmount(value)}
              placeholder="100.00"
              required
              className="w-full"
            />
            <p className="text-xs text-gray-500 mt-1">
              Maximum transfer: $10,000 per transaction
            </p>
          </div>

          <div>
            <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-2">
              Message (Optional)
            </label>
            <Input
              id="message"
              type="text"
              value={message}
              onChange={(value) => setMessage(value)}
              placeholder="Payment description..."
              maxLength={100}
              className="w-full"
            />
            <p className="text-xs text-gray-500 mt-1">
              Up to 100 characters
            </p>
          </div>

          <div className="flex gap-3 pt-4">
            <Button
              type="button"
              onClick={onBack}
              className="flex-1 bg-gray-500 hover:bg-gray-600"
            >
              Back
            </Button>
            <Button
              type="submit"
              disabled={isLoading || !amount || !recipientAccount}
              className="flex-1"
            >
              {isLoading ? 'Processing...' : 'Transfer Money'}
            </Button>
          </div>
        </form>
      </div>
    </Card>
  );
};

export default MoneyTransfer;
