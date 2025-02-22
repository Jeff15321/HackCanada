import React from 'react';
import { Model } from '../../../types/ModelType';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';

interface ItemMenuProps {
  models: Model[];
}

const ItemMenu: React.FC<ItemMenuProps> = ({ models }) => {
  const handleCardClick = (model: Model) => {
    // Handle card click - can be expanded later
    console.log('Viewing model:', model);
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 pb-6">
      {models.map((model) => (
        <div 
          key={model.id}
          onClick={() => handleCardClick(model)}
          className="group relative bg-gray-800/50 rounded-xl overflow-hidden 
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
          <div className="p-3 bg-gray-900/90 backdrop-blur-sm border-t border-cyan-400/20">
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
      ))}
    </div>
  );
};

export default ItemMenu;


