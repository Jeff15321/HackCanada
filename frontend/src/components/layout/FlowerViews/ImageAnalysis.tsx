import React, { useState, useEffect } from 'react';
import LocalFloristIcon from '@mui/icons-material/LocalFlorist';
import OpacityIcon from '@mui/icons-material/Opacity';
import WbSunnyIcon from '@mui/icons-material/WbSunny';
import TimelapseIcon from '@mui/icons-material/Timelapse';
import { useModel } from '@/contexts/ModelContext';


/* 
  Ensure you add these keyframes in your global CSS or Tailwind config:
  
  @keyframes slideRight {
    from { width: 0%; }
    to { width: var(--target-width); }
  }
*/

type Rarity = 'Garbage' | 'Common' | 'Rare' | 'Epic' | 'Legendary';

export const RARITY_COLORS: Record<Rarity, string> = {
  Garbage: '#808080',
  Common: '#3498db',
  Rare: '#e67e22',
  Epic: '#9b59b6',
  Legendary: '#f1c40f'
};

// Using Tailwind gradients for the overlay background per rarity
const RARITY_BACKGROUNDS: Record<Rarity, string> = {
  Garbage: 'bg-gradient-to-r from-gray-100 to-gray-200',
  Common: 'bg-gradient-to-r from-blue-100 to-blue-200',
  Rare: 'bg-gradient-to-r from-orange-100 to-orange-200',
  Epic: 'bg-gradient-to-r from-purple-100 to-purple-200',
  Legendary: 'bg-gradient-to-r from-yellow-100 to-yellow-200'
};

// Additional card styles based on rarity
const RARITY_CARD_STYLES: Record<Rarity, string> = {
  Garbage: 'border-gray-400',
  Common: 'border-blue-400',
  Rare: 'border-orange-400',
  Epic: 'border-purple-400',
  Legendary: 'border-yellow-400 shadow-2xl'
};

const TRAIT_RARITY_COLORS: Record<number, string> = {
  1: RARITY_COLORS.Common,      // Common
  2: '#2ecc71',                 // Uncommon
  3: RARITY_COLORS.Rare,        // Rare
  4: RARITY_COLORS.Epic,        // Epic
  5: RARITY_COLORS.Legendary    // Legendary
};

export const calculateRarity = (stats: { health: number; waterLevel: number; sunlight: number; growth: number }): Rarity => {
  const average = (stats.health + stats.waterLevel + stats.sunlight + stats.growth) / 4;
  if (average >= 55) return 'Legendary';
  if (average >= 45) return 'Epic';
  if (average >= 30) return 'Rare';
  if (average >= 20) return 'Common';
  return 'Garbage';
};

const generateRandomStats = () => {
  const generateStat = () => {
    let stat = 0;
    for (let i = 0; i < 3; i++) {
      stat += Math.random() * 100;
    }
    return Math.min(100, Math.floor(stat / 3));
  };
  
  return {
    health: generateStat(),
    growth: generateStat(),
    waterLevel: generateStat(),
    sunlight: generateStat()
  };
};

const AnimatedStat: React.FC<{ value: number; label: string; color: string }> = ({ value, label, color }) => {
  const [count, setCount] = useState(0);
  const { model } = useModel();
  
  useEffect(() => {
    const duration = 1500;
    const steps = 60;
    const increment = value / steps;
    const stepDuration = duration / steps;
    let currentStep = 0;

    const timer = setInterval(() => {
      currentStep++;
      if (currentStep === steps) {
        setCount(value);
        clearInterval(timer);
      } else {
        setCount(Math.min(Math.floor(increment * currentStep), value));
      }
    }, stepDuration);

    return () => clearInterval(timer);
  }, [value]);

  return (
    <div className="flex items-center gap-2">
      <div className="flex-1">
        <p className="text-sm text-gray-600">{label}</p>
        <div className="w-full h-2 rounded overflow-hidden bg-gray-200">
          <div 
            className="h-full" 
            style={{ 
              width: `${value}%`,
              backgroundColor: color,
              animation: 'slideRight 1.5s ease-out',
              transformOrigin: 'left'
            }}
          />
        </div>
      </div>
      <p className="min-w-[3rem] font-bold" style={{ color }}>{count}%</p>
    </div>
  );
};

// Add this type at the top with other interfaces
type AttributeType = 'shape' | 'color' | 'health' | 'development';

const ImageAnalysis: React.FC = () => {
  const { model } = useModel();
  
  // Get stats from model attributes
  const stats = {
    health: model?.attributes?.health || 0,
    waterLevel: model?.attributes?.shape || 0,
    sunlight: model?.attributes?.color || 0,
    growth: model?.attributes?.development || 0
  };

  const rarity = calculateRarity(stats);
  const rarityColor = RARITY_COLORS[rarity];

  const flowerData = {
    name: model?.name || "Crypto Rose",
    rarity,
    health: stats.health,
    shape: stats.waterLevel,
    color: stats.sunlight,
    development: stats.growth,
    traits: model?.attributes?.attributes || [],
    status: stats.health > 70 ? "Thriving" : "Struggling",
  };

  // Add state for selected attribute
  const [selectedAttribute, setSelectedAttribute] = useState<AttributeType | null>(null);
  
  // Add this function to get the description from the model
  const getAttributeDescription = () => {
    if (!selectedAttribute || !model?.description) return null;
    try {
      const data = JSON.parse(model.description);
      return data[selectedAttribute]?.analysis || null;
    } catch (error) {
      console.error('Error parsing description:', error);
      return null;
    }
  };

  return (
    <div className={`h-[85vh] rounded-lg relative bg-white bg-opacity-90 backdrop-blur-md border ${RARITY_CARD_STYLES[rarity]}`}>
      {/* Background overlay */}
      <div className="absolute inset-0 pointer-events-none rounded-lg" style={{ background: RARITY_BACKGROUNDS[rarity] }}></div>
      
      <div className="flex flex-col md:flex-row h-full p-4">
        {/* Left: Image Display */}
        <div className="w-full md:w-7/12 p-4 flex items-center justify-center border-b md:border-b-0 md:border-r border-gray-200">
          <div className="rounded-md overflow-hidden shadow-lg">
            <img src={model?.imageUrl} alt="Analyzed Flower" className="object-contain max-h-[70vh]" />
          </div>
        </div>

        {/* Right: Analysis */}
        <div className="w-full md:w-5/12 p-4 flex flex-col gap-3">
          {/* Vital Stats */}
          <div className="flex flex-col gap-2">
            <h2 className="text-xl text-gray-800">Vital Statistics</h2>
            <div 
              className="cursor-pointer transition-all hover:opacity-80"
              onClick={() => setSelectedAttribute('health')}
            >
              <AnimatedStat 
                value={flowerData.health} 
                label="Health" 
                color={selectedAttribute === 'health' ? rarityColor : '#666'} 
              />
            </div>
            <div 
              className="cursor-pointer transition-all hover:opacity-80"
              onClick={() => setSelectedAttribute('shape')}
            >
              <div className="flex items-center gap-2">
                <OpacityIcon className="text-[#1B998B]" />
                <AnimatedStat 
                  value={flowerData.shape} 
                  label="Shape & Structure" 
                  color={selectedAttribute === 'shape' ? rarityColor : '#666'} 
                />
              </div>
            </div>
            <div 
              className="cursor-pointer transition-all hover:opacity-80"
              onClick={() => setSelectedAttribute('color')}
            >
              <div className="flex items-center gap-2">
                <WbSunnyIcon className="text-[#1B998B]" />
                <AnimatedStat 
                  value={flowerData.color} 
                  label="Color & Texture" 
                  color={selectedAttribute === 'color' ? rarityColor : '#666'} 
                />
              </div>
            </div>
            <div 
              className="cursor-pointer transition-all hover:opacity-80"
              onClick={() => setSelectedAttribute('development')}
            >
              <div className="flex items-center gap-2">
                <TimelapseIcon className="text-[#1B998B]" />
                <AnimatedStat 
                  value={flowerData.development} 
                  label="Development" 
                  color={selectedAttribute === 'development' ? rarityColor : '#666'} 
                />
              </div>
            </div>
          </div>

          <hr className="border-t border-gray-200" />

          {/* Special Traits */}
          <div>
            <h2 className="text-xl text-gray-800">Special Traits</h2>
            <div className="flex flex-wrap gap-2 mt-2">
              {flowerData.traits.map((trait, index) => {
                const traitColor = TRAIT_RARITY_COLORS[trait.rarity] || rarityColor;
                return (
                  <span
                    key={index}
                    className={`
                      py-1.5 px-3 rounded-lg text-sm font-medium
                      transition-all duration-300 hover:scale-105
                      ${trait.rarity === 5 ? 'shadow-lg' : ''}
                    `}
                    style={{ 
                      backgroundColor: `${traitColor}15`,
                      color: traitColor,
                      borderWidth: '1.5px',
                      borderStyle: 'solid',
                      borderColor: `${traitColor}40`,
                      boxShadow: trait.rarity === 5 ? `0 0 10px ${traitColor}30` : 'none'
                    }}
                  >
                    <span className="font-bold">{trait.attribute}</span>
                    <span className="opacity-75 ml-1">({trait.rarity})</span>
                  </span>
                );
              })}
            </div>
          </div>

          <hr className="border-t border-gray-200" />

          {/* Attribute Description */}
          <div className="mt-2">
            <h2 className="text-xl text-gray-800 mb-2">Analysis Details</h2>
            <div className={`
              p-4 rounded-lg transition-all duration-300
              h-[20vh] overflow-y-auto
              ${selectedAttribute 
                ? 'bg-white/50 border border-gray-200' 
                : 'bg-gray-100/50 border border-gray-200/50'
              }
            `}>
              {selectedAttribute ? (
                <p className="text-gray-700">{getAttributeDescription()}</p>
              ) : (
                <p className="text-gray-500 italic">Click on any attribute above to see its detailed analysis</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImageAnalysis;
