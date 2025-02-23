import React, { useEffect, useState } from 'react';
import { getOwnerTokens } from '@/services/api';
import { useUser } from '@/contexts/UserContext';
import WalletLogin from '../auth/WalletLogin';
import { TokenData } from '@/types/TokenTypes';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';
import SearchIcon from '@mui/icons-material/Search';

const TokenCollection: React.FC = () => {
  const [tokens, setTokens] = useState<TokenData[]>([]);
  const [loading, setLoading] = useState(true);
  const { user } = useUser();
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchTokens = async () => {
      if (user?.id) {
        try {
          const response = await getOwnerTokens("hackcanada.testnet");
          const tokenArray = Array.isArray(response) ? response :
                           response?.token ? response.token :
                           response?.tokens ? response.tokens :
                           [];
          setTokens(tokenArray);
          console.log("Tokens:", tokenArray);
        } catch (error) {
          console.error('Error fetching tokens:', error);
          setTokens([]);
        } finally {
          setLoading(false);
        }
      }
    };

    fetchTokens();
  }, [user?.id]);

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
                      NFT Collection
                    </h1>
                    <p className="text-cyan-400">
                      View your minted NFTs
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-gray-400">Total NFTs</p>
                  <p className="text-2xl font-bold text-white">{tokens.length}</p>
                </div>
              </div>

              {/* Search Bar */}
              <div className="relative mt-6">
                <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 text-cyan-400/50" />
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Search collection..."
                  className="w-full pl-10 pr-4 py-2 rounded-lg bg-gray-800/50 border border-cyan-400/20
                    text-white placeholder-gray-400 focus:border-cyan-400 focus:outline-none transition-colors duration-300"
                />
              </div>
            </div>

            {loading ? (
              <div className="flex items-center justify-center min-h-[400px]">
                <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-cyan-500"></div>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 p-8">
                {tokens.map((token) => (
                  <div
                    key={token.token_id}
                    className="bg-gray-800/30 backdrop-blur-sm rounded-xl overflow-hidden
                      border border-cyan-400/20 hover:border-cyan-400/40 
                      transition-all duration-300 group cursor-pointer"
                  >
                    <div className="aspect-square relative">
                      <img
                        src={token.metadata.media}
                        alt={token.metadata.title}
                        className="w-full h-full object-cover"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-gray-900 to-transparent opacity-0 
                        group-hover:opacity-100 transition-opacity duration-300" />
                    </div>

                    <div className="p-4">
                      <h3 className="text-lg font-semibold text-white group-hover:text-cyan-400 
                        transition-colors duration-300">
                        {token.metadata.title}
                      </h3>
                      <p className="text-gray-400 text-sm mt-1 line-clamp-2">
                        {token.metadata.description}
                      </p>
                      <div className="flex items-center justify-between mt-4">
                        {token.metadata.price && (
                          <div className="text-cyan-400 font-medium">
                            {parseFloat(token.metadata.price) / 1e24} NEAR
                          </div>
                        )}
                        <div className="text-xs text-gray-500">
                          #{token.token_id.split('-').pop()}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}

                {tokens.length === 0 && (
                  <div className="col-span-full text-center text-gray-400 py-12">
                    <p className="text-xl">No NFTs found in your collection</p>
                    <p className="mt-2">Start minting some flowers to see them here!</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </WalletLogin>
  );
};

export default TokenCollection; 