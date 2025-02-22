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
    <div className="flex-col h-full">
      {/* Flower Name and Rarity */}
      <div className="flex-1">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">{model?.name || "Unnamed Flower"}</h1>
          <span
            className={`inline-block mt-1 py-1 px-3 text-sm font-bold text-white rounded ${rarity === 'Legendary' ? 'border border-white/50 shadow-lg' : ''}`}
            style={{ backgroundColor: rarityColor }}
          >
            {rarity}
          </span>
        </div>
      </div>

      <div className="h-full p-8">
        <div className="h-full rounded-2xl bg-white/90 backdrop-blur-sm border border-purple-200 shadow-xl p-8">
          <div className="flex flex-col h-full">
            {/* Value Display */}
            <div className="flex-1 space-y-6">
              <h2 className="text-2xl font-bold text-gray-800">Flower Value</h2>
              <div className="bg-purple-50 rounded-xl p-6 border border-purple-100">
                <div className="text-5xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
                  ${value.toLocaleString()}
                </div>
                <div className="text-sm text-purple-600 mt-2 font-medium">
                  Estimated market value
                </div>
              </div>
            </div>

            {/* Buttons */}
            <div className="space-y-4 mt-8">
              <Button
                variant="outlined"
                fullWidth
                size="large"
                startIcon={<ViewInAr className="text-2xl" />}
                onClick={onVRView}
                className="h-14 text-lg font-semibold rounded-xl"
                sx={{
                  borderColor: '#9333ea',
                  borderWidth: '2px',
                  color: '#9333ea',
                  '&:hover': {
                    borderWidth: '2px',
                    borderColor: '#7e22ce',
                    backgroundColor: 'rgba(147, 51, 234, 0.04)'
                  }
                }}
              >
                View in VR
              </Button>

              <Button
                variant="contained"
                fullWidth
                size="large"
                startIcon={<ShoppingCart className="text-2xl" />}
                onClick={onPurchase}
                className="h-14 text-lg font-semibold rounded-xl"
                sx={{
                  background: 'linear-gradient(to right, #9333ea, #6366f1)',
                  '&:hover': {
                    background: 'linear-gradient(to right, #7e22ce, #4f46e5)'
                  }
                }}
              >
                Purchase Now
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Payment; 