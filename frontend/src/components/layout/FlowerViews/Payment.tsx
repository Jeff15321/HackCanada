import React, { useState } from 'react';
import { Button } from '@mui/material';
import { ViewInAr, ShoppingCart, CheckCircle, ErrorOutline, CloseRounded } from '@mui/icons-material';
import { useModel } from '../../../contexts/ModelContext';
import { calculateRarity, RARITY_COLORS } from './ImageAnalysis';
import { useUser } from '@/contexts/UserContext';
import axios from 'axios';
import { Model } from '@/types/ModelType';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const Payment: React.FC = () => {
  const { model, setModel } = useModel() as { model: Model | null; setModel: (model: Model | null) => void };
  const { user } = useUser();
  const [purchaseStatus, setPurchaseStatus] = useState<'idle' | 'success' | 'failed'>('idle');
  
  const isOwner = user?.id === model?.walletID;

  const stats = {
    colorVibrancy: model?.parameters?.colorVibrancy || { score: 0, explanation: '' },
    leafAreaIndex: model?.parameters?.leafAreaIndex || { score: 0, explanation: '' },
    wilting: model?.parameters?.wilting || { score: 0, explanation: '' },
    spotting: model?.parameters?.spotting || { score: 0, explanation: '' },
    symmetry: model?.parameters?.symmetry || { score: 0, explanation: '' }
  };

  const rarity = calculateRarity(stats);
  const rarityColor = RARITY_COLORS[rarity];

  const handlePurchase = async () => {
    if (!model?.id) {
      setPurchaseStatus('failed');
      return;
    }

    let buyerId = user?.id;
    if (!buyerId) {
      const localUser = localStorage.getItem('user');
      if (localUser) {
        try {
          const userData = JSON.parse(localUser);
          buyerId = userData.id;
        } catch (e) {
          setPurchaseStatus('failed');
          return;
        }
      } else {
        setPurchaseStatus('failed');
        return;
      }
    }

    try {
      if (!buyerId) {
        setPurchaseStatus('failed');
        return;
      }

      const formData = new FormData();
      formData.append('new_owner_id', buyerId);

      await axios.post(
        `${API_BASE_URL}/v1/model/${model.id}/update-owner`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      setPurchaseStatus('success');
      // Update local model data
      setModel({
        ...model,
        walletID: buyerId
      });
    } catch (error) {
      console.error('Error updating owner:', error);
      setPurchaseStatus('failed');
    }
  };

  return (
    <div className="flex flex-col gap-4 h-full">
      {/* Success Popup */}
      {purchaseStatus === 'success' && (
        <div 
          className="fixed inset-0 flex items-center justify-center bg-black/50 z-50"
          onClick={() => setPurchaseStatus('idle')}
        >
          <div 
            className="bg-gray-900 rounded-xl border border-cyan-400/20 p-8 max-w-md w-full mx-4 relative"
            onClick={e => e.stopPropagation()}
          >
            <button
              onClick={() => setPurchaseStatus('idle')}
              className="absolute top-4 right-4 text-gray-400 hover:text-white"
            >
              <CloseRounded />
            </button>
            <CheckCircle className="text-green-500 w-20 h-20 mb-4 mx-auto" />
            <h2 className="text-2xl font-bold text-white mb-2 text-center">Purchase Successful!</h2>
            <p className="text-gray-400 text-center">
              Your flower has been added to your collection
            </p>
          </div>
        </div>
      )}

      {/* Failed Popup */}
      {purchaseStatus === 'failed' && (
        <div 
          className="fixed inset-0 flex items-center justify-center bg-black/50 z-50"
          onClick={() => setPurchaseStatus('idle')}
        >
          <div 
            className="bg-gray-900 rounded-xl border border-cyan-400/20 p-8 max-w-md w-full mx-4 relative"
            onClick={e => e.stopPropagation()}
          >
            <button
              onClick={() => setPurchaseStatus('idle')}
              className="absolute top-4 right-4 text-gray-400 hover:text-white"
            >
              <CloseRounded />
            </button>
            <ErrorOutline className="text-red-500 w-20 h-20 mb-4 mx-auto" />
            <h2 className="text-2xl font-bold text-white mb-2 text-center">Purchase Failed</h2>
            <p className="text-gray-400 text-center mb-4">
              Please login to purchase this flower
            </p>
            <button
              onClick={() => setPurchaseStatus('idle')}
              className="w-full px-6 py-2 bg-cyan-500 hover:bg-cyan-600 text-white rounded-lg"
            >
              Try Again
            </button>
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
              onClick={handlePurchase}
              disabled={isOwner}
              className={`w-full h-[7rem] flex items-center justify-center gap-2 
                ${isOwner 
                  ? 'bg-gray-600 cursor-not-allowed' 
                  : 'bg-cyan-500 hover:bg-cyan-600'} 
                text-white rounded-lg
                border border-cyan-400/50 transition-all duration-300`}
            >
              <ShoppingCart />
              <span>{isOwner ? "Already Owned" : "Purchase Now"}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Payment; 