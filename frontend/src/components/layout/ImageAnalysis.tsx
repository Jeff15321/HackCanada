import React, { useState, useEffect } from 'react';
import LocalFloristIcon from '@mui/icons-material/LocalFlorist';
import OpacityIcon from '@mui/icons-material/Opacity';
import WbSunnyIcon from '@mui/icons-material/WbSunny';
import TimelapseIcon from '@mui/icons-material/Timelapse';

interface ImageAnalysisProps {
  imageUrl: string;
}

/* 
  Ensure you add these keyframes in your global CSS or Tailwind config:
  
  @keyframes slideRight {
    from { width: 0%; }
    to { width: var(--target-width); }
  }
*/

type Rarity = 'Garbage' | 'Common' | 'Rare' | 'Epic' | 'Legendary';

const RARITY_COLORS: Record<Rarity, string> = {
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

const calculateRarity = (stats: { health: number; waterLevel: number; sunlight: number; growth: number }): Rarity => {
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

const ImageAnalysis: React.FC<ImageAnalysisProps> = ({ imageUrl }) => {
  const stats = generateRandomStats();
  const rarity = calculateRarity(stats);
  const rarityColor = RARITY_COLORS[rarity];

  const flowerData = {
    name: "Crypto Rose",
    rarity,
    health: stats.health,
    growth: stats.growth,
    waterLevel: stats.waterLevel,
    sunlight: stats.sunlight,
    traits: ["Fast Growing", "Rare Color", "High Yield"],
    status: stats.health > 70 ? "Thriving" : "Struggling",
  };

  return (
    <div className={`max-w-5xl mx-auto rounded-lg relative bg-white bg-opacity-90 backdrop-blur-md border ${RARITY_CARD_STYLES[rarity]}`}>
      {/* Background overlay */}
      <div className="absolute inset-0 pointer-events-none" style={{ background: RARITY_BACKGROUNDS[rarity] }}></div>
      
      <div className="flex flex-col md:flex-row min-h-[600px] p-4">
        {/* Left: Image Display */}
        <div className="w-full md:w-7/12 p-4 flex items-center justify-center border-b md:border-b-0 md:border-r border-gray-200">
          <div className="rounded-md overflow-hidden shadow-lg">
            <img src={imageUrl} alt="Analyzed Flower" className="object-contain max-h-[80vh]" />
          </div>
        </div>

        {/* Right: Analysis */}
        <div className="w-full md:w-5/12 p-4 flex flex-col gap-3">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">{flowerData.name}</h1>
            <span
              className={`inline-block mt-1 py-1 px-3 text-sm font-bold text-white rounded ${rarity === 'Legendary' ? 'border border-white/50 shadow-lg' : ''}`}
              style={{ backgroundColor: rarityColor }}
            >
              {flowerData.rarity}
            </span>
          </div>

          <div className="flex items-center gap-2">
            <LocalFloristIcon style={{ color: flowerData.status === 'Thriving' ? '#1B998B' : '#FF9800' }} />
            <h2 className="text-xl" style={{ color: flowerData.status === 'Thriving' ? '#1B998B' : '#FF9800' }}>
              Status: {flowerData.status}
            </h2>
          </div>

          <hr className="border-t border-gray-200" />

          {/* Vital Stats */}
          <div className="flex flex-col gap-2">
            <h2 className="text-xl text-gray-800">Vital Statistics</h2>
            <AnimatedStat value={flowerData.health} label="Health" color={rarityColor} />
            <div className="flex items-center gap-2">
              <OpacityIcon className="text-[#1B998B]" />
              <AnimatedStat value={flowerData.waterLevel} label="Water Level" color={rarityColor} />
            </div>
            <div className="flex items-center gap-2">
              <WbSunnyIcon className="text-[#1B998B]" />
              <AnimatedStat value={flowerData.sunlight} label="Sunlight" color={rarityColor} />
            </div>
            <div className="flex items-center gap-2">
              <TimelapseIcon className="text-[#1B998B]" />
              <AnimatedStat value={flowerData.growth} label="Growth" color={rarityColor} />
            </div>
          </div>

          <hr className="border-t border-gray-200" />

          {/* Traits */}
          <div>
            <h2 className="text-xl text-gray-800">Special Traits</h2>
            <div className="flex flex-wrap gap-2 mt-2">
              {flowerData.traits.map((trait, index) => (
                <span
                  key={index}
                  className="py-1 px-2 rounded text-sm"
                  style={{ backgroundColor: `${rarityColor}20`, color: rarityColor }}
                >
                  {trait}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImageAnalysis;
