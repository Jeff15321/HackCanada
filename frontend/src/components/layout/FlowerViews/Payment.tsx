import React from 'react';
import { Button } from '@mui/material';
import { ViewInAr, ShoppingCart } from '@mui/icons-material';
import { useModel } from '../../../contexts/ModelContext';
import { calculateRarity, RARITY_COLORS } from './ImageAnalysis';

interface PaymentProps {
  value: number;
  onVRView?: () => void;
  onPurchase?: () => void;
}

const Payment: React.FC<PaymentProps> = ({ 
  value = 1500, // Default value for testing
  onVRView = () => console.log('VR View clicked'),
  onPurchase = () => console.log('Purchase clicked')
}) => {
  const { model } = useModel();
  
  // Calculate rarity and color based on stats
  const stats = {
    health: model?.attributes?.health || 0,
    waterLevel: model?.attributes?.shape || 0,
    sunlight: model?.attributes?.color || 0,
    growth: model?.attributes?.development || 0
  };

  const rarity = calculateRarity(stats);
  const rarityColor = RARITY_COLORS[rarity];

  return (
    <div className="flex flex-col gap-4 h-full">
      {/* Top Box - Name and Rarity */}
      <div className="bg-gray-900 rounded-xl border border-cyan-400/20 p-6">
        <div className="flex flex-col gap-6 py-6 justify-between items-start">
          <h1 className="text-3xl font-bold text-white">{model?.name || "Unnamed Flower"}</h1>
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
            <h2 className="text-lg text-gray-400 mb-2">Estimated Value</h2>
            <div className="bg-gray-800 rounded-xl p-4 border border-cyan-400/20">
              <div className="text-4xl font-bold text-white">
                {value.toLocaleString()} ETH
              </div>
              <div className="text-sm text-cyan-400 mt-1">
                ≈ ${(value * 2800).toLocaleString()} USD
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="space-y-3 mt-auto pt-6">
            <button
              onClick={onPurchase}
              className="w-full h-12 flex items-center justify-center gap-2 
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