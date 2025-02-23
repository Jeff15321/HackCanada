import React from 'react';
import { Model } from '../../../types/ModelType';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';
import { useModel } from '@/contexts/ModelContext';
import { useRouter } from 'next/router';
import { calculateRarity, RARITY_COLORS } from './ImageAnalysis';

interface ItemMenuProps {
  models: Model[];
}

const ItemMenu: React.FC<ItemMenuProps> = ({ models }) => {
  const { setModel } = useModel();
  const router = useRouter();

  const handleCardClick = (model: Model) => {
    setModel(model);
    router.push(`/image/${model.id}`);
  };

  const getRarityColor = (model: Model) => {
    const stats = {
      health: model?.attributes?.health || 0,
      waterLevel: model?.attributes?.shape || 0,
      sunlight: model?.attributes?.color || 0,
      growth: model?.attributes?.development || 0
    };
    const rarity = calculateRarity(stats);
    return RARITY_COLORS[rarity];
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 pb-6">
      {models.map((model) => {
        const rarityColor = getRarityColor(model);
        return (
          <div 
            key={model.id}
            onClick={() => handleCardClick(model)}
            className="group relative bg-gray-900 rounded-xl overflow-hidden 
              shadow-lg hover:shadow-2xl transition-all duration-300 hover:scale-105
              border border-cyan-400/20 backdrop-blur-sm cursor-pointer"
          >
            {/* Image */}
            <div className="w-full h-[40vh] overflow-hidden">
              <img 
                src={model.imageUrl} 
                alt={model.name}
                className="w-full h-full object-cover transform group-hover:scale-110 
                  transition-transform duration-300"
              />
            </div>

            {/* Content */}
            <div 
              className="p-3 backdrop-blur-sm"
              style={{ 
                background: `linear-gradient(to right, ${rarityColor}70, ${rarityColor}90)`,
                borderTop: `2px solid ${rarityColor}`
              }}
            >
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-base font-bold text-white">
                  {model.name}
                </h3>
                <AccountBalanceWalletIcon className="text-cyan-400 text-xl" />
              </div>
              
              <div>
                <p className="text-xs text-gray-400">Price</p>
                <p className="text-base font-bold text-white">
                  {Math.floor(1000 + Math.random() * 9000)} ETH
                </p>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default ItemMenu;


