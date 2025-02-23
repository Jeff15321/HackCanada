import React from 'react';
import { Button } from '@mui/material';
import { ViewInAr, ShoppingCart } from '@mui/icons-material';
import { useModel } from '../../../contexts/ModelContext';
import { calculateRarity, RARITY_COLORS } from './ImageAnalysis';

const Payment: React.FC = () => {
  const { model } = useModel();
  
  const stats = {
    colorVibrancy: model?.parameters?.colorVibrancy || { score: 0, explanation: '' },
    leafAreaIndex: model?.parameters?.leafAreaIndex || { score: 0, explanation: '' },
    wilting: model?.parameters?.wilting || { score: 0, explanation: '' },
    spotting: model?.parameters?.spotting || { score: 0, explanation: '' },
    symmetry: model?.parameters?.symmetry || { score: 0, explanation: '' }
  };

  const rarity = calculateRarity(stats);
  const rarityColor = RARITY_COLORS[rarity];

  return (
    <div className="flex flex-col gap-4 h-full">
      {/* Top Box - Name and Rarity */}
      <div className="bg-gray-900 rounded-xl border border-cyan-400/20 p-6">
        <div className="flex flex-col gap-6 py-6 justify-between items-start">
          <h1 className="text-3xl font-bold text-white">{model?.name}</h1>
          <span
            className="px-3 py-1 text-xl font-bold rounded-lg bg-gray-800"
            style={{ color: rarityColor, borderColor: `${rarityColor}40` }}
          >
            {rarity}
          </span>
        </div>
      </div>

      {/* Bottom Box - Payment Details */}
      <div className="flex-1 bg-gray-900 rounded-xl border border-cyan-400/20 p-6">
        <div className="flex flex-col h-full">
          {/* Value Display */}
          <div className="flex-1">
            <h2 className="text-2xl text-gray-400 my-8">Estimated Value</h2>
            <div className="bg-gray-800 rounded-xl p-8 border border-cyan-400/20">
              <div className="text-4xl font-bold text-white">
                {(Number(model?.price) / 10000).toLocaleString()} ETH
              </div>
              <div className="text-sm text-cyan-400 mt-1">
                ≈ ${((Number(model?.price) / 10000) * 2800).toLocaleString()} USD
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="space-y-3 mt-auto pt-6">
            <button
              onClick={() => console.log('Purchase clicked')}
              className="w-full h-[7rem] flex items-center justify-center gap-2 
                bg-cyan-500 hover:bg-cyan-600 text-white rounded-lg
                border border-cyan-400/50 transition-all duration-300"
            >
              <ShoppingCart />
              <span>Purchase Now</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Payment; 