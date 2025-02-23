import React, { useState } from 'react';
import { Button } from '@mui/material';
import { ViewInAr, ShoppingCart, CheckCircle } from '@mui/icons-material';
import { useModel } from '../../../contexts/ModelContext';
import { calculateRarity, RARITY_COLORS } from './ImageAnalysis';
import { mintNFT } from '../../../services/api';

const Payment: React.FC = () => {
  const { model } = useModel();
  const [showSuccess, setShowSuccess] = useState(false);

  const handlePurchase = () => {
    // if (!model?.id || !model?.name || !model?.glbFileUrl || !model?.walletID) {
    //   console.error('Missing required model data');
    //   return;
    // }
       
    // (async () => {
    //   try {
    //     const response = await mintNFT(
    //       Math.random().toString(36).substring(2, 15),
    //       "your-account.testnet",
    //       "https://example.com/plant.glb",
    //       "Test Plant NFT",
    //       "your-account.testnet",
    //       "1000000000000000000000000",
    //       {
    //         color_vibrancy: { score: 85, explanation: "Vibrant color" },
    //         leaf_area_index: { score: 90, explanation: "High coverage" },
    //         wilting: { score: 5, explanation: "No wilting" },
    //         spotting: { score: 2, explanation: "Minor spots" },
    //         symmetry: { score: 92, explanation: "Well balanced" }
    //       }
    //     );

    //     console.log("NFT Minted Successfully:", response);
    //   } catch (error) {
    //     console.error("Minting failed:", error);
    //   }
    // })();


    
    // setShowSuccess(true);
    // setTimeout(() => setShowSuccess(false), 3000);
  }
  
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
    <div className="relative flex flex-col gap-4 h-full">
      {/* Success Popup */}
      {showSuccess && (
        <div className="fixed inset-0 flex items-center justify-center z-50">
          <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" />
          <div className="relative bg-gray-900 rounded-xl border border-cyan-400/20 p-8 flex flex-col items-center gap-4 animate-fadeIn">
            <CheckCircle className="text-cyan-400 text-6xl animate-bounce" />
            <h2 className="text-2xl font-bold text-white">Purchase Successful!</h2>
            <p className="text-cyan-400">Your NFT has been minted</p>
          </div>
        </div>
      )}

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
              onClick={() => handlePurchase()}
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