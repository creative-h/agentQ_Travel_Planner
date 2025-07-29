import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  CreditCardIcon, UpiIcon, WalletIcon, ShoppingBagIcon, 
  BanknotesIcon, CheckCircleIcon, LinkIcon
} from '../icons';
import { PAYMENT_METHODS } from '../../types';

const CheckoutPage = ({ selectedPackage, tripDetails, onClose }) => {
  const [paymentMethod, setPaymentMethod] = useState(PAYMENT_METHODS.CREDIT_CARD);
  const [formData, setFormData] = useState({
    cardNumber: '',
    cardName: '',
    expiryDate: '',
    cvv: '',
    upiId: '',
    email: ''
  });
  const [isProcessing, setIsProcessing] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const navigate = useNavigate();
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };
  
  const handlePaymentMethodChange = (method) => {
    setPaymentMethod(method);
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    setIsProcessing(true);
    
    // Simulate payment processing
    setTimeout(() => {
      setIsProcessing(false);
      setIsComplete(true);
      
      // Redirect after successful payment simulation
      setTimeout(() => {
        navigate('/dashboard'); // Redirect to dashboard or success page
      }, 3000);
    }, 2000);
  };
  
  // Payment method option component
  const PaymentOption = ({ method, icon, label, selected, onChange }) => (
    <div 
      className={`flex items-center p-4 border rounded-lg cursor-pointer transition-all ${
        selected ? 'border-indigo-600 bg-indigo-50' : 'border-gray-200 hover:bg-gray-50'
      }`}
      onClick={() => onChange(method)}
    >
      <div className={`p-2 rounded-full mr-3 ${selected ? 'bg-indigo-100 text-indigo-600' : 'bg-gray-100 text-gray-500'}`}>
        {icon}
      </div>
      <div className="flex-grow">
        <p className={`font-medium ${selected ? 'text-indigo-600' : 'text-gray-700'}`}>{label}</p>
      </div>
      <div className="w-5 h-5 border-2 rounded-full flex items-center justify-center">
        {selected && <div className="w-3 h-3 bg-indigo-600 rounded-full"></div>}
      </div>
    </div>
  );
  
  if (isComplete) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-xl w-full max-w-lg p-8">
          <div className="text-center">
            <div className="bg-green-100 p-3 rounded-full inline-flex mb-4">
              <CheckCircleIcon className="h-12 w-12 text-green-600" />
            </div>
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Payment Successful!</h2>
            <p className="text-gray-600 mb-6">Your booking has been confirmed. You will receive a confirmation email shortly.</p>
            <div className="p-4 bg-gray-50 rounded-lg mb-6">
              <div className="flex justify-between mb-2">
                <span className="text-gray-600">Booking Reference:</span>
                <span className="font-semibold">{`TR-${Math.floor(100000 + Math.random() * 900000)}`}</span>
              </div>
              <div className="flex justify-between mb-2">
                <span className="text-gray-600">Amount Paid:</span>
                <span className="font-semibold">${selectedPackage.totalPrice.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Payment Method:</span>
                <span className="font-semibold">{
                  paymentMethod === PAYMENT_METHODS.CREDIT_CARD ? 'Credit Card' :
                  paymentMethod === PAYMENT_METHODS.UPI ? 'UPI' : 'Wallet'
                }</span>
              </div>
            </div>
            <button 
              className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition-colors"
              onClick={() => navigate('/dashboard')}
            >
              View My Bookings
            </button>
          </div>
        </div>
      </div>
    );
  }
  
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl my-8">
        <div className="flex flex-col md:flex-row">
          {/* Order Summary */}
          <div className="w-full md:w-2/5 bg-gray-50 p-6 rounded-l-lg">
            <div className="flex items-center mb-6">
              <ShoppingBagIcon className="h-6 w-6 text-indigo-600 mr-2" />
              <h2 className="text-xl font-bold text-gray-800">Order Summary</h2>
            </div>
            
            <div className="mb-6">
              <h3 className="font-semibold text-gray-700 mb-2">{selectedPackage.name}</h3>
              <p className="text-sm text-gray-600 mb-4">{selectedPackage.description}</p>
              
              <div className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Package Type:</span>
                  <span className="font-medium text-gray-800 capitalize">{selectedPackage.type}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Destination:</span>
                  <span className="font-medium text-gray-800">{selectedPackage.destination}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Travel Dates:</span>
                  <span className="font-medium text-gray-800">{selectedPackage.flight.departureDate} - {selectedPackage.flight.returnDate}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Flight:</span>
                  <span className="font-medium text-gray-800">{selectedPackage.flight.airline}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Hotel:</span>
                  <span className="font-medium text-gray-800">{selectedPackage.hotel.name}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Nights:</span>
                  <span className="font-medium text-gray-800">{selectedPackage.hotel.numberOfNights}</span>
                </div>
              </div>
            </div>
            
            <div className="border-t border-gray-200 pt-4 mb-6">
              <div className="flex justify-between mb-2">
                <span className="text-gray-600">Flight Cost:</span>
                <span className="font-medium">${selectedPackage.flight.price.toLocaleString()}</span>
              </div>
              <div className="flex justify-between mb-2">
                <span className="text-gray-600">Hotel Cost:</span>
                <span className="font-medium">${(selectedPackage.hotel.pricePerNight * selectedPackage.hotel.numberOfNights).toLocaleString()}</span>
              </div>
              <div className="flex justify-between mb-2">
                <span className="text-gray-600">Taxes & Fees:</span>
                <span className="font-medium">${(selectedPackage.totalPrice - selectedPackage.flight.price - (selectedPackage.hotel.pricePerNight * selectedPackage.hotel.numberOfNights)).toLocaleString()}</span>
              </div>
              <div className="flex justify-between text-lg font-bold mt-4 pt-4 border-t border-gray-200">
                <span className="text-gray-800">Total:</span>
                <span className="text-indigo-600">${selectedPackage.totalPrice.toLocaleString()}</span>
              </div>
            </div>
            
            <div className="flex items-center text-xs text-gray-500">
              <LinkIcon className="h-4 w-4 mr-1" />
              <span>Secured by TripyTrek Payment Gateway</span>
            </div>
          </div>
          
          {/* Payment Form */}
          <div className="w-full md:w-3/5 p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold text-gray-800">Payment Details</h2>
              <button 
                onClick={onClose}
                className="text-gray-500 hover:text-gray-700"
              >
                &times; Close
              </button>
            </div>
            
            <div className="mb-6">
              <h3 className="font-medium text-gray-700 mb-3">Select Payment Method</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                <PaymentOption 
                  method={PAYMENT_METHODS.CREDIT_CARD}
                  icon={<CreditCardIcon className="h-6 w-6" />}
                  label="Credit Card"
                  selected={paymentMethod === PAYMENT_METHODS.CREDIT_CARD}
                  onChange={handlePaymentMethodChange}
                />
                <PaymentOption 
                  method={PAYMENT_METHODS.UPI}
                  icon={<UpiIcon className="h-6 w-6" />}
                  label="UPI"
                  selected={paymentMethod === PAYMENT_METHODS.UPI}
                  onChange={handlePaymentMethodChange}
                />
                <PaymentOption 
                  method={PAYMENT_METHODS.WALLET}
                  icon={<WalletIcon className="h-6 w-6" />}
                  label="Wallet"
                  selected={paymentMethod === PAYMENT_METHODS.WALLET}
                  onChange={handlePaymentMethodChange}
                />
              </div>
            </div>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              {paymentMethod === PAYMENT_METHODS.CREDIT_CARD && (
                <>
                  <div>
                    <label htmlFor="cardName" className="block text-sm font-medium text-gray-700 mb-1">Name on Card</label>
                    <input 
                      type="text" 
                      id="cardName" 
                      name="cardName" 
                      value={formData.cardName}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      placeholder="John Doe"
                      required 
                    />
                  </div>
                  <div>
                    <label htmlFor="cardNumber" className="block text-sm font-medium text-gray-700 mb-1">Card Number</label>
                    <input 
                      type="text" 
                      id="cardNumber" 
                      name="cardNumber" 
                      value={formData.cardNumber}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      placeholder="1234 5678 9012 3456"
                      required 
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label htmlFor="expiryDate" className="block text-sm font-medium text-gray-700 mb-1">Expiry Date</label>
                      <input 
                        type="text" 
                        id="expiryDate" 
                        name="expiryDate" 
                        value={formData.expiryDate}
                        onChange={handleInputChange}
                        className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        placeholder="MM/YY"
                        required 
                      />
                    </div>
                    <div>
                      <label htmlFor="cvv" className="block text-sm font-medium text-gray-700 mb-1">CVV</label>
                      <input 
                        type="text" 
                        id="cvv" 
                        name="cvv" 
                        value={formData.cvv}
                        onChange={handleInputChange}
                        className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        placeholder="123"
                        required 
                      />
                    </div>
                  </div>
                </>
              )}
              
              {paymentMethod === PAYMENT_METHODS.UPI && (
                <div>
                  <label htmlFor="upiId" className="block text-sm font-medium text-gray-700 mb-1">UPI ID</label>
                  <input 
                    type="text" 
                    id="upiId" 
                    name="upiId" 
                    value={formData.upiId}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    placeholder="yourname@upi"
                    required 
                  />
                </div>
              )}
              
              {paymentMethod === PAYMENT_METHODS.WALLET && (
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
                  <input 
                    type="email" 
                    id="email" 
                    name="email" 
                    value={formData.email}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    placeholder="you@example.com"
                    required 
                  />
                  <p className="mt-2 text-sm text-gray-500">We'll redirect you to your wallet provider to complete the payment.</p>
                </div>
              )}
              
              <div className="mt-8">
                <button 
                  type="submit" 
                  className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition-colors flex items-center justify-center"
                  disabled={isProcessing}
                >
                  {isProcessing ? (
                    <>
                      <svg className="animate-spin h-5 w-5 mr-3 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Processing...
                    </>
                  ) : (
                    <>
                      <BanknotesIcon className="h-5 w-5 mr-2" />
                      Pay ${selectedPackage.totalPrice.toLocaleString()}
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CheckoutPage;
