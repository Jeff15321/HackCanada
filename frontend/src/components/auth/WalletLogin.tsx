import React, { useEffect, useState } from 'react';
import { useUser } from '@/contexts/UserContext';

const WalletLogin = ({ children }: { children: React.ReactNode }) => {
  const { user, setUser } = useUser();
  const [inputValue, setInputValue] = useState('');

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    console.log(user);
  }, []);

  if (!user) {
    return (
      <div className="min-h-screen w-full flex items-center justify-center">
        <div className="bg-gray-900 rounded-xl p-8 border border-cyan-400/20 w-full max-w-md mx-4">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">Connect Wallet</h2>
          <input
            type="text"
            placeholder="Enter your crypto key..."
            className="w-full px-4 py-3 rounded-lg bg-gray-800 border border-cyan-400/20
              text-white placeholder-gray-400 mb-4
              focus:border-cyan-400 focus:outline-none transition-all"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
          <button 
            onClick={() => {
              setUser({ id: inputValue });
              localStorage.setItem('user', JSON.stringify({ id: inputValue }));
            }}
            className="w-full py-3 bg-cyan-500 hover:bg-cyan-600 
              text-white rounded-lg transition-all duration-300
              border border-cyan-400/50 font-medium"
          >
            Connect
          </button>
        </div>
      </div>
    );
  }

  return <>{children}</>;
};

export default WalletLogin; 