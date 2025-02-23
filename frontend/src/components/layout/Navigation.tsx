import React from 'react';
import StorefrontIcon from '@mui/icons-material/Storefront';
import CollectionsIcon from '@mui/icons-material/Collections';
import AddIcon from '@mui/icons-material/Add';
import TokenIcon from '@mui/icons-material/Token';
import { useRouter } from 'next/router';

type Tab = 'marketplace' | 'collection' | 'profile' | 'tokens';

interface NavigationProps {
  activeTab: Tab;
  onTabChange: (tab: Tab) => void;
}

const Navigation: React.FC<NavigationProps> = ({ activeTab, onTabChange }) => {
  const router = useRouter();

  const navItems = [
    { id: 'marketplace', icon: StorefrontIcon, tooltip: 'NFT Marketplace' },
    { id: 'collection', icon: CollectionsIcon, tooltip: 'My Collection' },
    { id: 'profile', icon: AddIcon, tooltip: 'Create New' },
    { id: 'tokens', icon: TokenIcon, tooltip: 'NFT Tokens', path: '/tokencollection' }
  ];

  const handleClick = (id: string) => {
    if (id === 'tokens') {
      router.push('/tokencollection');
    } else {
      onTabChange(id as Tab);
    }
  };

  return (
    <div className="fixed left-4 top-1/2 -translate-y-1/2 flex flex-col gap-4 z-50">
      {/* Cyber line decoration */}
      <div className="absolute -left-2 -top-32 w-[2px] h-[140%] bg-cyan-400/20">
        <div className="absolute top-0 left-0 w-full h-1/3 animate-pulse bg-gradient-to-b from-cyan-400 to-transparent" />
      </div>

      {navItems.map(({ id, icon: Icon, tooltip }) => (
        <div key={id} className="group relative">
          <button
            onClick={() => handleClick(id)}
            className={`
              w-14 h-14 rounded-xl flex items-center justify-center
              transition-all duration-300 transform hover:scale-110
              border border-cyan-400/20 backdrop-blur-sm
              ${activeTab === id 
                ? 'bg-cyan-500 text-white shadow-lg shadow-cyan-400/20' 
                : 'bg-gray-900/50 text-gray-400 hover:text-cyan-400'}
            `}
          >
            <Icon className={`text-2xl transition-transform duration-300 ${activeTab === id ? 'scale-110' : ''}`} />
          </button>
          
          {/* Tooltip */}
          <div className="absolute left-16 top-1/2 -translate-y-1/2 px-3 py-1.5 
            bg-gray-900 text-cyan-400 text-sm rounded-lg
            opacity-0 invisible group-hover:opacity-100 group-hover:visible 
            transition-all duration-300 whitespace-nowrap
            border border-cyan-400/20">
            {tooltip}
          </div>
        </div>
      ))}
    </div>
  );
};

export default Navigation; 