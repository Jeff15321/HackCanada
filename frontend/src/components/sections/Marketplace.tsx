import React, { useEffect, useState } from 'react';
import { fetchAllModels } from '../../services/api';
import { Model } from '../../types/ModelType';
import ItemMenu from '../layout/FlowerViews/ItemMenu';
import { useUser } from '@/contexts/UserContext';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';
import SearchIcon from '@mui/icons-material/Search';
import { calculateRarity } from '../layout/FlowerViews/ImageAnalysis';

// New component for the search/filter bar
const SearchBar = ({ onSearch }: { onSearch: (query: string, rarity: string) => void }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRarity, setSelectedRarity] = useState('All Rarities');

  const handleSearch = () => {
    onSearch(searchQuery, selectedRarity);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="bg-gray-900/50 backdrop-blur-md rounded-xl p-4 mb-8 
      border border-cyan-400/20">
      <div className="flex flex-wrap gap-4">
        <div className="flex-1 min-w-[200px] relative">
          <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 text-cyan-400/50" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Search NFTs..."
            className="w-full pl-10 pr-4 py-2 rounded-lg 
              bg-gray-800/50 border border-cyan-400/20
              text-white placeholder-gray-400
              focus:border-cyan-400 focus:outline-none 
              transition-colors duration-300"
          />
        </div>
        <select 
          value={selectedRarity}
          onChange={(e) => {
            setSelectedRarity(e.target.value);
            onSearch(searchQuery, e.target.value);
          }}
          className="px-4 py-2 rounded-lg 
            bg-gray-800/50 border border-cyan-400/20
            text-white focus:border-cyan-400 focus:outline-none 
            transition-colors duration-300"
        >
          <option>All Rarities</option>
          <option>Legendary</option>
          <option>Epic</option>
          <option>Rare</option>
          <option>Common</option>
          <option>Garbage</option>
        </select>
        <button 
          onClick={handleSearch}
          className="px-6 py-2 bg-cyan-500 hover:bg-cyan-600 
            text-white rounded-lg transition-colors duration-300
            border border-cyan-400/50"
        >
          Search
        </button>
      </div>
    </div>
  );
};

const Marketplace = () => {
  const [models, setModels] = useState<Model[]>([]);
  const [filteredModels, setFilteredModels] = useState<Model[]>([]);
  const { user } = useUser();

  useEffect(() => {
    const loadModels = async () => {
      const fetchedModels = await fetchAllModels();
      const userModels = fetchedModels.filter((model) => model.id !== user?.id);
      setModels(userModels);
      setFilteredModels(userModels);
    };
    loadModels();
  }, [user?.id]);

  const handleSearch = (query: string, rarity: string) => {
    let filtered = [...models];

    // Filter by name
    if (query) {
      filtered = filtered.filter(model => 
        model.name.toLowerCase().includes(query.toLowerCase())
      );
    }

    // Filter by rarity
    if (rarity !== 'All Rarities') {
      filtered = filtered.filter(model => {
        const stats = {
          colorVibrancy: model.parameters.colorVibrancy,
          leafAreaIndex: model.parameters.leafAreaIndex,
          wilting: model.parameters.wilting,
          spotting: model.parameters.spotting,
          symmetry: model.parameters.symmetry
        };
        return calculateRarity(stats) === rarity;
      });
    }

    setFilteredModels(filtered);
  };

  return (
    <div className="min-h-screen bg-transparent">
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
            </div>
          </div>

          {/* Search Bar */}
          <SearchBar onSearch={handleSearch} />

          {/* Content */}
          <div className="max-w-7xl mx-auto">
            <ItemMenu models={filteredModels} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Marketplace; 