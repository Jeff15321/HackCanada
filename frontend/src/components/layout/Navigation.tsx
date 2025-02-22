import React from 'react';

type Tab = 'marketplace' | 'collection' | 'profile';

interface NavigationProps {
  activeTab: Tab;
  onTabChange: (tab: Tab) => void;
}

const Navigation: React.FC<NavigationProps> = ({ activeTab, onTabChange }) => {
  return (
    <div className="w-full flex justify-center gap-4">
      {['marketplace', 'collection', 'profile'].map((tab) => (
        <button
          key={tab}
          onClick={() => onTabChange(tab as Tab)}
          className={`
            w-48 py-3 px-6 rounded-lg font-semibold text-lg
            transition-all duration-300 transform hover:scale-105
            ${activeTab === tab 
              ? 'bg-purple-600 text-white shadow-lg' 
              : 'bg-white/80 text-gray-700 hover:bg-white'}
          `}
        >
          {tab.charAt(0).toUpperCase() + tab.slice(1)}
        </button>
      ))}
    </div>
  );
};

export default Navigation; 