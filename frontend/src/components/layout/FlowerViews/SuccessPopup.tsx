import React from 'react';
import { CheckCircle } from '@mui/icons-material';

interface SuccessPopupProps {
  show: boolean;
}

const SuccessPopup: React.FC<SuccessPopupProps> = ({ show }) => {
  if (!show) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center z-50">
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" />
      <div className="relative bg-gray-900 rounded-xl border border-cyan-400/20 p-8 flex flex-col items-center gap-4 animate-fadeIn">
        <CheckCircle className="text-cyan-400 text-6xl animate-bounce" />
        <h2 className="text-2xl font-bold text-white">Purchase Successful!</h2>
        <p className="text-cyan-400">Your NFT has been minted</p>
      </div>
    </div>
  );
};

export default SuccessPopup; 