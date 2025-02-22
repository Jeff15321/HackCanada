import React, { useEffect, useState } from 'react';
import { fetchAllModels } from '../../services/api';
import { Model } from '../../types/ModelType';
import ItemMenu from '../layout/FlowerViews/ItemMenu';
import { useUser } from '@/contexts/UserContext';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';
import SearchIcon from '@mui/icons-material/Search';

// New component for the search/filter bar
const SearchBar = () => {
  return (
    <div className="bg-gray-900/50 backdrop-blur-md rounded-xl p-4 mb-8 
      border border-cyan-400/20">
      <div className="flex flex-wrap gap-4">
        <div className="flex-1 min-w-[200px] relative">
          <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 text-cyan-400/50" />
          <input
            type="text"
            placeholder="Search NFTs..."
            className="w-full pl-10 pr-4 py-2 rounded-lg 
              bg-gray-800/50 border border-cyan-400/20
              text-white placeholder-gray-400
              focus:border-cyan-400 focus:outline-none 
              transition-colors duration-300"
          />
        </div>
        <select className="px-4 py-2 rounded-lg 
          bg-gray-800/50 border border-cyan-400/20
          text-white focus:border-cyan-400 focus:outline-none 
          transition-colors duration-300">
          <option>All Rarities</option>
          <option>Common</option>
          <option>Rare</option>
          <option>Epic</option>
          <option>Legendary</option>
        </select>
        <button className="px-6 py-2 bg-cyan-500 hover:bg-cyan-600 
          text-white rounded-lg transition-colors duration-300
          border border-cyan-400/50">
          Search
        </button>
      </div>
    </div>
  );
};

const Marketplace = () => {
  const [models, setModels] = useState<Model[]>([]);
  const { user } = useUser();

  useEffect(() => {
    const loadModels = async () => {
      const fetchedModels = await fetchAllModels();
      setModels(fetchedModels.filter((model) => model.id !== user?.id));
    };
    loadModels();
  }, []);

  return (
    <div className="min-h-screen bg-black">
      <div className="h-full flex flex-col">
        <div className="flex-1 overflow-y-auto scrollbar-hide">
          {/* Header */}
          <div className="p-8 bg-gray-800/30 backdrop-blur-sm rounded-xl mb-8
            border border-cyan-400/20">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-xl bg-cyan-400/10 
                  flex items-center justify-center border border-cyan-400/20">
                  <AccountBalanceWalletIcon className="text-3xl text-cyan-400" />
                </div>
                <div>
                  <h1 className="text-3xl font-bold text-white">
                    NFT Marketplace
                  </h1>
                  <p className="text-cyan-400">
                    Discover and collect unique digital flowers
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-gray-400">Floor Price</p>
                <p className="text-2xl font-bold text-white">2.5 ETH</p>
              </div>
            </div>
          </div>

          {/* Search Bar */}
          <SearchBar />

          {/* Content */}
          <div className="max-w-7xl mx-auto">
            <ItemMenu models={models} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Marketplace; 