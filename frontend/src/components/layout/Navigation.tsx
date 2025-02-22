import React from 'react';
import StorefrontIcon from '@mui/icons-material/Storefront';
import CollectionsIcon from '@mui/icons-material/Collections';
import PersonIcon from '@mui/icons-material/Person';

type Tab = 'marketplace' | 'collection' | 'profile';

interface NavigationProps {
  activeTab: Tab;
  onTabChange: (tab: Tab) => void;
}

const Navigation: React.FC<NavigationProps> = ({ activeTab, onTabChange }) => {
  const navItems = [
    { id: 'marketplace', icon: StorefrontIcon, tooltip: 'NFT Marketplace' },
    { id: 'collection', icon: CollectionsIcon, tooltip: 'My Collection' },
    { id: 'profile', icon: PersonIcon, tooltip: 'Wallet Profile' }
  ];

  return (
    <div className="fixed left-4 top-1/2 -translate-y-1/2 flex flex-col gap-6 z-50">
      {/* Cyber line decoration */}
      <div className="absolute -left-2 -top-32 w-[2px] h-[140%] bg-cyan-400/20">
        <div className="absolute top-0 left-0 w-full h-1/3 animate-pulse bg-gradient-to-b from-cyan-400 to-transparent" />
      </div>

      {navItems.map(({ id, icon: Icon, tooltip }) => (
        <div key={id} className="group relative">
          {/* Tooltip */}
          <div className="absolute left-16 top-1/2 -translate-y-1/2 px-4 py-2 
            bg-gray-900/90 text-cyan-400 text-sm rounded-md
            opacity-0 invisible group-hover:opacity-100 group-hover:visible 
            transition-all duration-300 whitespace-nowrap
            border border-cyan-400/20 backdrop-blur-sm">
            {tooltip}
            <div className="absolute left-0 top-1/2 -translate-x-1 -translate-y-1/2 
              border-[6px] border-transparent border-r-gray-900/90" />
          </div>

          <button
            onClick={() => onTabChange(id as Tab)}
            className={`
              w-12 h-12 rounded-xl flex items-center justify-center
              transition-all duration-300 transform hover:scale-110
              border border-cyan-400/20 backdrop-blur-sm
              before:absolute before:inset-0 before:rounded-xl
              before:bg-gradient-to-r before:from-cyan-400/0 before:to-cyan-400/0
              before:opacity-0 before:transition-opacity before:duration-300
              hover:before:opacity-100 overflow-hidden
              ${activeTab === id 
                ? 'bg-gray-900 text-cyan-400 shadow-lg shadow-cyan-400/20' 
                : 'bg-gray-900/50 text-gray-400 hover:text-cyan-400'}
            `}
          >
            <Icon className={`text-2xl transition-transform duration-300 ${activeTab === id ? 'scale-110' : ''}`} />
            
            {/* Cyber corner accents */}
            <div className="absolute top-0 left-0 w-2 h-2 border-t-2 border-l-2 border-cyan-400/50" />
            <div className="absolute top-0 right-0 w-2 h-2 border-t-2 border-r-2 border-cyan-400/50" />
            <div className="absolute bottom-0 left-0 w-2 h-2 border-b-2 border-l-2 border-cyan-400/50" />
            <div className="absolute bottom-0 right-0 w-2 h-2 border-b-2 border-r-2 border-cyan-400/50" />
          </button>
        </div>
      ))}
    </div>
  );
};

export default Navigation; 