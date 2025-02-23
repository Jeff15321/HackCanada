import React, { useEffect, useState } from 'react';
import { fetchAllModels } from '../../services/api';
import { Model } from '../../types/ModelType';
import ItemMenu from '../layout/FlowerViews/ItemMenu';
import { useUser } from '@/contexts/UserContext';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';
import SearchIcon from '@mui/icons-material/Search';
import WalletLogin from '../auth/WalletLogin';
import { searchModels } from '@/utils/search';
import { calculateRarity } from '../layout/FlowerViews/ImageAnalysis';
import { runPipelineViaBackend, getOwnerTokens  } from '@/services/api';
// Add interface for SearchBar props
interface MarketProps {
  searchTerm: string;
  setSearchTerm: (term: string) => void;
  rarityFilter: string;
  setRarityFilter: (rarity: string) => void;
}

const SearchBar = ({ searchTerm, setSearchTerm, rarityFilter, setRarityFilter }: MarketProps) => {
  return (
    <div className="bg-gray-900/50 backdrop-blur-md rounded-xl p-4 mb-8 border border-cyan-400/20">

      <div className="flex flex-wrap gap-4">
        <div className="flex-1 min-w-[200px] relative">
          <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 text-cyan-400/50" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search marketplace..."
            className="w-full pl-10 pr-4 py-2 rounded-lg bg-gray-800/50 border border-cyan-400/20
              text-white placeholder-gray-400 focus:border-cyan-400 focus:outline-none transition-colors duration-300"
          />
        </div>
        <select
          value={rarityFilter}
          onChange={(e) => setRarityFilter(e.target.value)}
          className="px-4 py-2 rounded-lg bg-gray-800/50 border border-cyan-400/20
            text-white focus:border-cyan-400 focus:outline-none transition-colors duration-300"
        >
          <option value="">All Rarities</option>
          <option value="common">Common</option>
          <option value="rare">Rare</option>
          <option value="epic">Epic</option>
          <option value="legendary">Legendary</option>
        </select>
      </div>
    </div>
  );
};

const Marketplace = () => {
  const [models, setModels] = useState<Model[]>([]);
  const { user } = useUser();
  const [searchTerm, setSearchTerm] = useState('');
  const [rarityFilter, setRarityFilter] = useState('');

  useEffect(() => {
    if (user) {
      const loadModels = async () => {
        const fetchedModels = await fetchAllModels();
        setModels(fetchedModels.filter((model) => model.walletID !== user?.id));
      };
      loadModels();
    }
  }, [user]);

  const filteredModels = models
    .filter(model => {
      const matchesSearch = searchTerm ? 
        model.name.toLowerCase().includes(searchTerm.toLowerCase()) : true;

      const rarity = calculateRarity({
        colorVibrancy: model.parameters?.colorVibrancy || { score: 0, explanation: '' },
        leafAreaIndex: model.parameters?.leafAreaIndex || { score: 0, explanation: '' },
        wilting: model.parameters?.wilting || { score: 0, explanation: '' },
        spotting: model.parameters?.spotting || { score: 0, explanation: '' },
        symmetry: model.parameters?.symmetry || { score: 0, explanation: '' }
      }).toLowerCase();

      const matchesRarity = rarityFilter ? rarity === rarityFilter.toLowerCase() : true;

      return matchesSearch && matchesRarity;
    })
    .reverse();

  return (
    <WalletLogin>
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
                <div className="text-right">
                  <p className="text-gray-400">Total Items</p>
                  <p className="text-2xl font-bold text-white">{models.length}</p>
                </div>
              </div>
            </div>

            {/* Search Bar */}
            <SearchBar 
              searchTerm={searchTerm} 
              setSearchTerm={setSearchTerm}
              rarityFilter={rarityFilter}
              setRarityFilter={setRarityFilter}
            />

            {/* Content */}
            <div className="max-w-7xl mx-auto">
              <ItemMenu models={filteredModels} />
            </div>
          </div>
        </div>
      </div>
    </WalletLogin>
  );
};

export default Marketplace; 