import React, { useState, useEffect } from 'react';
import { Card, Button } from '../ui';
import { accountsService } from '../../services/accounts';
import { useError, useLoading } from '../../context';
import type { 
  TimeDeposit, 
  CreateTimeDepositRequest,
  InterestRateConfig
} from '../../types';
import { INTEREST_RATES } from '../../types/transfer';

interface TimeDepositsProps {
  accountNumber: string;
  onBack: () => void;
}

const TimeDeposits: React.FC<TimeDepositsProps> = ({ accountNumber, onBack }) => {
  const [deposits, setDeposits] = useState<TimeDeposit[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({
    amount: '',
    duration_months: 6,
    is_test_deposit: false
  });
  const { setError } = useError();
  const { setGlobalLoading } = useLoading();

  // Load time deposits on mount
  useEffect(() => {
    loadTimeDeposits();
  }, []);

  const loadTimeDeposits = async () => {
    try {
      setGlobalLoading(true, 'Loading time deposits...');
      const response = await accountsService.listTimeDeposits(accountNumber);
      setDeposits(response.data.deposits || []);
    } catch (error: any) {
      setError(error.detail || 'Failed to load time deposits');
    } finally {
      setGlobalLoading(false);
      setIsLoading(false);
    }
  };

  const handleCreateDeposit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const validation = accountsService.validateAmount(formData.amount);
    if (!validation.isValid) {
      setError(validation.error || 'Invalid amount');
      return;
    }

    try {
      setGlobalLoading(true, 'Creating time deposit...');
      
      const request: CreateTimeDepositRequest = {
        amount: validation.numericValue!,
        duration_months: formData.duration_months,
        is_test_deposit: formData.is_test_deposit
      };
      
      await accountsService.createTimeDeposit(accountNumber, request);
      
      // Reload deposits
      await loadTimeDeposits();
      
      // Reset form
      setFormData({ amount: '', duration_months: 6, is_test_deposit: false });
      setShowCreateForm(false);
      
    } catch (error: any) {
      setError(error.detail || 'Failed to create time deposit');
    } finally {
      setGlobalLoading(false);
    }
  };

  const handleMatureDeposit = async (depositId: string) => {
    try {
      setGlobalLoading(true, 'Maturing time deposit...');
      await accountsService.matureTimeDeposit(depositId);
      await loadTimeDeposits();
    } catch (error: any) {
      setError(error.detail || 'Failed to mature time deposit');
    } finally {
      setGlobalLoading(false);
    }
  };

  const getInterestRateInfo = (durationMonths: number): InterestRateConfig | undefined => {
    return INTEREST_RATES.find(rate => rate.duration_months === durationMonths);
  };

  const calculateProjectedEarnings = (amount: number, durationMonths: number): number => {
    const rateInfo = getInterestRateInfo(durationMonths);
    if (!rateInfo) return amount;
    
    return accountsService.calculateTimeDepositEarnings(
      amount, 
      rateInfo.interest_rate, 
      durationMonths
    );
  };

  if (isLoading) {
    return (
      <Card title="Loading Time Deposits..." description="Please wait while we load your deposits.">
        <div className="text-center py-8">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card
        title="Time Deposits"
        description={`Manage time deposits for account ${accountNumber}`}
      >
        <div className="flex justify-between items-center mb-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-800">
              Your Time Deposits ({deposits.length})
            </h3>
            <p className="text-sm text-gray-600 mt-1">
              Earn guaranteed returns with our competitive interest rates
            </p>
          </div>
          <Button 
            variant="primary"
            onClick={() => setShowCreateForm(!showCreateForm)}
          >
            {showCreateForm ? 'Cancel' : 'Create New Deposit'}
          </Button>
        </div>

        {/* Create Form */}
        {showCreateForm && (
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 mb-6">
            <h4 className="text-md font-semibold text-gray-800 mb-4">Create New Time Deposit</h4>
            
            <form onSubmit={handleCreateDeposit} className="space-y-4">
              <div>
                <label htmlFor="amount" className="block text-sm font-medium text-gray-700 mb-2">
                  Deposit Amount
                </label>
                <input
                  type="number"
                  id="amount"
                  step="0.01"
                  min="1"
                  max="100000"
                  value={formData.amount}
                  onChange={(e) => setFormData(prev => ({ ...prev, amount: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Enter amount (min $1, max $100,000)"
                  required
                />
              </div>

              <div>
                <label htmlFor="duration" className="block text-sm font-medium text-gray-700 mb-2">
                  Duration & Interest Rate
                </label>
                <select
                  id="duration"
                  value={formData.duration_months}
                  onChange={(e) => setFormData(prev => ({ ...prev, duration_months: parseInt(e.target.value) }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  disabled={formData.is_test_deposit}
                >
                  {INTEREST_RATES.map(rate => (
                    <option key={rate.duration_months} value={rate.duration_months}>
                      {rate.description}
                    </option>
                  ))}
                </select>
              </div>

              {/* Test Deposit Toggle */}
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="testDeposit"
                    checked={formData.is_test_deposit}
                    onChange={(e) => setFormData(prev => ({ 
                      ...prev, 
                      is_test_deposit: e.target.checked,
                      duration_months: e.target.checked ? 1 : 6  // Set to 1 month for test deposits
                    }))}
                    className="h-4 w-4 text-yellow-600 focus:ring-yellow-500 border-gray-300 rounded"
                  />
                  <label htmlFor="testDeposit" className="ml-2 block text-sm text-gray-700">
                    <span className="font-medium">Quick Test Deposit</span>
                    <span className="block text-xs text-gray-500 mt-1">
                      Creates a deposit that matures in 1 second for testing purposes
                    </span>
                  </label>
                </div>
                {formData.is_test_deposit && (
                  <div className="mt-2 text-xs text-yellow-700 bg-yellow-100 rounded p-2">
                    ⚡ Test mode: This deposit will mature immediately for testing the maturity process.
                  </div>
                )}
              </div>

              {/* Projection */}
              {formData.amount && !isNaN(parseFloat(formData.amount)) && (
                <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
                  <h5 className="font-medium text-primary-800 mb-2">
                    {formData.is_test_deposit ? 'Test Deposit Preview' : 'Projected Earnings'}
                  </h5>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-primary-600">Principal:</span>
                      <span className="font-mono ml-2">
                        {accountsService.formatCurrency(parseFloat(formData.amount))}
                      </span>
                    </div>
                    <div>
                      <span className="text-primary-600">Final Amount:</span>
                      <span className="font-mono ml-2 font-bold">
                        {accountsService.formatCurrency(
                          calculateProjectedEarnings(parseFloat(formData.amount), formData.duration_months)
                        )}
                      </span>
                    </div>
                  </div>
                  {formData.is_test_deposit && (
                    <div className="mt-2 text-xs text-primary-700">
                      This deposit will be available for immediate maturity testing.
                    </div>
                  )}
                </div>
              )}

              <div className="flex gap-3">
                <Button type="submit" variant="primary">
                  Create Deposit
                </Button>
                <Button 
                  type="button" 
                  variant="outline"
                  onClick={() => setShowCreateForm(false)}
                >
                  Cancel
                </Button>
              </div>
            </form>
          </div>
        )}

        {/* Deposits List */}
        {deposits.length === 0 ? (
          <div className="text-center py-12 bg-gray-50 rounded-lg">
            <svg className="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 className="text-lg font-medium text-gray-800 mb-2">No Time Deposits Yet</h3>
            <p className="text-gray-600">Start earning guaranteed returns by creating your first time deposit.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {deposits.map(deposit => {
              const projectedFinal = calculateProjectedEarnings(deposit.amount, deposit.duration_months);
              const isMatured = deposit.is_matured;
              const maturityDate = accountsService.formatMaturityDate(deposit.created_at, deposit.duration_months);
              const isCloseToMaturity = accountsService.isCloseToMaturity(deposit.maturity_date);
              const isTestDeposit = new Date(deposit.maturity_date).getTime() - new Date(deposit.created_at).getTime() < 60000; // Less than 1 minute
              const canMatureNow = new Date() >= new Date(deposit.maturity_date) && !isMatured;

              return (
                <div 
                  key={deposit.deposit_id}
                  className={`border rounded-lg p-6 ${
                    isMatured ? 'bg-green-50 border-green-200' : 
                    canMatureNow ? 'bg-blue-50 border-blue-200' :
                    isCloseToMaturity ? 'bg-yellow-50 border-yellow-200' : 
                    'bg-white border-gray-200'
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-3">
                        <h4 className="text-lg font-semibold text-gray-800">
                          Deposit #{deposit.deposit_id.slice(-6)}
                        </h4>
                        {isTestDeposit && (
                          <span className="px-2 py-1 text-xs font-medium rounded-full bg-orange-100 text-orange-800">
                            Test Deposit
                          </span>
                        )}
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                          isMatured ? 'bg-green-100 text-green-800' :
                          canMatureNow ? 'bg-blue-100 text-blue-800' :
                          isCloseToMaturity ? 'bg-yellow-100 text-yellow-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {isMatured ? 'Matured' : 
                           canMatureNow ? 'Ready to Mature' :
                           isCloseToMaturity ? 'Close to Maturity' : 'Active'}
                        </span>
                      </div>

                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        <div>
                          <span className="text-gray-600">Principal:</span>
                          <div className="font-mono font-bold">
                            {accountsService.formatCurrency(deposit.amount)}
                          </div>
                        </div>
                        <div>
                          <span className="text-gray-600">Duration:</span>
                          <div className="font-semibold">{deposit.duration_months} months</div>
                        </div>
                        <div>
                          <span className="text-gray-600">Interest Rate:</span>
                          <div className="font-semibold">
                            {(deposit.interest_rate * 100).toFixed(1)}% APY
                          </div>
                        </div>
                        <div>
                          <span className="text-gray-600">Final Amount:</span>
                          <div className="font-mono font-bold text-green-600">
                            {accountsService.formatCurrency(projectedFinal)}
                          </div>
                        </div>
                      </div>

                      <div className="mt-3 text-sm text-gray-600">
                        <span>Created: {new Date(deposit.created_at).toLocaleDateString()}</span>
                        <span className="mx-2">•</span>
                        <span>Matures: {maturityDate}</span>
                        {isTestDeposit && (
                          <>
                            <span className="mx-2">•</span>
                            <span className="text-orange-600 font-medium">Test Deposit</span>
                          </>
                        )}
                      </div>

                      {canMatureNow && (
                        <div className="mt-3 p-3 bg-blue-100 border border-blue-200 rounded-lg">
                          <div className="flex items-center text-blue-800">
                            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <span className="text-sm font-medium">
                              This deposit has reached maturity and can be processed!
                            </span>
                          </div>
                        </div>
                      )}
                    </div>

                    {!isMatured && (
                      <div className="ml-4 flex flex-col gap-2">
                        {canMatureNow ? (
                          <Button
                            size="sm"
                            variant="primary"
                            onClick={() => handleMatureDeposit(deposit.deposit_id)}
                          >
                            Mature Now
                          </Button>
                        ) : (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleMatureDeposit(deposit.deposit_id)}
                          >
                            Early Mature
                          </Button>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        <div className="mt-6 pt-6 border-t border-gray-200">
          <Button variant="outline" onClick={onBack}>
            Back to Dashboard
          </Button>
        </div>
      </Card>

      {/* Interest Rates Info */}
      <Card title="Current Interest Rates" description="Our competitive rates for time deposits">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {INTEREST_RATES.map(rate => (
            <div 
              key={rate.duration_months}
              className="text-center p-4 bg-gradient-to-br from-primary-50 to-primary-100 border border-primary-200 rounded-lg"
            >
              <div className="text-lg font-bold text-primary-700">
                {rate.duration_months} Month{rate.duration_months > 1 ? 's' : ''}
              </div>
              <div className="text-2xl font-bold text-primary-800 my-2">
                {(rate.interest_rate * 100).toFixed(1)}%
              </div>
              <div className="text-sm text-primary-600">APY</div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};

export default TimeDeposits;
