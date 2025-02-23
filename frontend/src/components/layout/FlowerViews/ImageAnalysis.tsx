import React, { useState, useEffect } from 'react';
import LocalFloristIcon from '@mui/icons-material/LocalFlorist';
import OpacityIcon from '@mui/icons-material/Opacity';
import WbSunnyIcon from '@mui/icons-material/WbSunny';
import TimelapseIcon from '@mui/icons-material/Timelapse';
import { useModel } from '@/contexts/ModelContext';
import { useRouter } from 'next/router';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { Model } from '@/types/ModelType';
import { useImage } from '@/contexts/ImageContext';


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

export const calculateRarity = (stats: { 
  colorVibrancy: { score: number; explanation: string };
  leafAreaIndex: { score: number; explanation: string };
  wilting: { score: number; explanation: string };
  spotting: { score: number; explanation: string };
  symmetry: { score: number; explanation: string };
}): Rarity => {
  const average = (
    stats.colorVibrancy.score + 
    stats.leafAreaIndex.score + 
    stats.wilting.score + 
    stats.spotting.score + 
    stats.symmetry.score
  ) / 5;

  if (average >= 80) return 'Legendary';
  if (average >= 60) return 'Epic';
  if (average >= 40) return 'Rare';
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

interface AnimatedStatProps {
  value: number;
  label: string;
  color: string;
}

const AnimatedStat: React.FC<AnimatedStatProps> = ({ value, label, color }) => {
  const [width, setWidth] = useState(0);
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    // Reset to 0 when value changes
    setWidth(0);
    setCount(0);

    // Animate to target value
    const duration = 1500;
    const steps = 60;
    const increment = value / steps;
    const stepDuration = duration / steps;
    let currentStep = 0;

    const timer = setInterval(() => {
      currentStep++;
      if (currentStep === steps) {
        setWidth(value);
        setCount(value);
        clearInterval(timer);
      } else {
        const newValue = Math.min(increment * currentStep, value);
        setWidth(newValue);
        setCount(Math.floor(newValue));
      }
    }, stepDuration);

    return () => clearInterval(timer);
  }, [value]);

  return (
    <div className="flex items-center gap-2">
      <div className="flex-1">
        <p className="text-sm text-gray-400">{label}</p>
        <div className="w-full h-2 rounded overflow-hidden bg-gray-800 border border-cyan-400/10">
          <div 
            className="h-full transition-all duration-[1500ms] ease-out"
            style={{ 
              width: `${width}%`,
              backgroundColor: color,
            }}
          />
        </div>
      </div>
      <p className="min-w-[3rem] font-bold text-white">{count}%</p>
    </div>
  );
};

// Add this type at the top with other interfaces
type AttributeType = 'colorVibrancy' | 'leafAreaIndex' | 'wilting' | 'spotting' | 'symmetry';

interface Trait {
  attribute: string;
  rarity: number;
}

interface ImageAnalysisProps {
  model: Model | null;  // Allow null
}

const ImageAnalysis: React.FC<ImageAnalysisProps> = ({ model }) => {
  const { model: contextModel } = useModel();
  const router = useRouter();
  const { imageUrl } = useImage();
  const [imageLoaded, setImageLoaded] = useState(false);
  const [displayUrl, setDisplayUrl] = useState<string | null>(null);
  
  const handleBack = () => {
    router.back();
  };

  // Get stats from model attributes
  const stats = {
    colorVibrancy: contextModel?.parameters?.colorVibrancy || { score: 0, explanation: '' },
    leafAreaIndex: contextModel?.parameters?.leafAreaIndex || { score: 0, explanation: '' },
    wilting: contextModel?.parameters?.wilting || { score: 0, explanation: '' },
    spotting: contextModel?.parameters?.spotting || { score: 0, explanation: '' },
    symmetry: contextModel?.parameters?.symmetry || { score: 0, explanation: '' }
  };

  const rarity = calculateRarity(stats);
  const rarityColor = RARITY_COLORS[rarity];

  const flowerData = {
    name: contextModel?.name || "Crypto Rose",
    rarity,
    health: stats.colorVibrancy.score,
    shape: stats.leafAreaIndex.score,
    color: stats.wilting.score,
    development: stats.spotting.score,
    traits: Array.isArray(contextModel?.special) ? contextModel.special : [],
    status: stats.colorVibrancy.score > 70 ? "Thriving" : "Struggling",
  };

  // Add state for selected attribute
  const [selectedAttribute, setSelectedAttribute] = useState<string | null>(null);
  
  // Add this function to get the description from the model
  const getAttributeDescription = () => {
    if (!selectedAttribute || !model?.parameters) return '';
    return model.parameters[selectedAttribute as keyof typeof model.parameters]?.explanation || '';
  };

  useEffect(() => {
    // Try loading glbFileUrl first
    if (model?.glbFileUrl) {
      const img = new Image();
      img.src = model.glbFileUrl;
      img.onload = () => {
        setDisplayUrl(model.glbFileUrl);
        setImageLoaded(true);
      };
      img.onerror = () => {
        // Fallback to imageUrl if glbFileUrl fails
        if (imageUrl) {
          setDisplayUrl(imageUrl);
          setImageLoaded(true);
        }
      };
    } else if (imageUrl) {
      // If no glbFileUrl, use imageUrl directly
      setDisplayUrl(imageUrl);
      setImageLoaded(true);
    }
  }, [model?.glbFileUrl, imageUrl]);

  return (
    <div className="relative w-full h-full">
      <div className={`h-[90vh] flex flex-row rounded-lg relative bg-gray-900 border border-cyan-400/20`}>
        {/* Left: Image Display */}
        <div className="w-full md:w-7/12 pl-6 flex flex-col">
          <div className="flex-1 flex items-center justify-center">
            <div className="relative w-full pt-[100%]">
              <div className="absolute inset-0 rounded-xl overflow-hidden shadow-2xl">
                <button 
                  onClick={handleBack}
                  className="absolute top-4 left-4 z-10 p-2
                    bg-gray-900/80 hover:bg-gray-800 text-white rounded-full
                    border border-cyan-400/20 backdrop-blur-sm transition-all duration-300
                    hover:scale-110"
                >
                  <ArrowBackIcon className="text-cyan-400 text-xl" />
                </button>

                {displayUrl && (
                  <img 
                    src={displayUrl}
                    alt={model?.name || "Flower"}
                    className="absolute inset-0 w-full h-full object-cover"
                  />
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Right: Analysis */}
        <div className="w-full md:w-5/12 p-6 flex flex-col h-full">
          {/* Main content wrapper with flex */}
          <div className="flex flex-col h-full gap-4">
            {/* Vital Stats - flex-grow-0 to maintain size */}
            <div className="flex-shrink-0">
              <div className="flex flex-col gap-3">
                <div 
                  className="cursor-pointer transition-all hover:opacity-80" 
                  onClick={() => setSelectedAttribute('colorVibrancy')}
                >
                  <AnimatedStat 
                    value={Math.floor(stats.colorVibrancy.score)}
                    label="Color Vibrancy" 
                    color={selectedAttribute === 'colorVibrancy' ? rarityColor : '#0ea5e9'}
                  />
                </div>
                <div 
                  className="cursor-pointer transition-all hover:opacity-80" 
                  onClick={() => setSelectedAttribute('leafAreaIndex')}
                >
                  <AnimatedStat 
                    value={Math.floor(stats.leafAreaIndex.score)}
                    label="Leaf Area Index" 
                    color={selectedAttribute === 'leafAreaIndex' ? rarityColor : '#0ea5e9'}
                  />
                </div>
                <div 
                  className="cursor-pointer transition-all hover:opacity-80" 
                  onClick={() => setSelectedAttribute('wilting')}
                >
                  <AnimatedStat 
                    value={Math.floor(stats.wilting.score)}
                    label="Wilting" 
                    color={selectedAttribute === 'wilting' ? rarityColor : '#0ea5e9'}
                  />
                </div>
                <div 
                  className="cursor-pointer transition-all hover:opacity-80" 
                  onClick={() => setSelectedAttribute('spotting')}
                >
                  <AnimatedStat 
                    value={Math.floor(stats.spotting.score)}
                    label="Spotting" 
                    color={selectedAttribute === 'spotting' ? rarityColor : '#0ea5e9'}
                  />
                </div>
                <div 
                  className="cursor-pointer transition-all hover:opacity-80" 
                  onClick={() => setSelectedAttribute('symmetry')}
                >
                  <AnimatedStat 
                    value={Math.floor(stats.symmetry.score)}
                    label="Symmetry" 
                    color={selectedAttribute === 'symmetry' ? rarityColor : '#0ea5e9'}
                  />
                </div>
              </div>
            </div>

            <hr className="border-t border-gray-700" />

            {/* Special Traits - flex-grow-0 to maintain size */}
            <div className="flex-shrink-0">
              <div className="bg-gray-800/50 rounded-xl p-3 border border-cyan-400/20">
                <div className="flex flex-wrap gap-2">
                  {flowerData.traits.map((trait: Trait, index: number) => {
                    const traitColor = TRAIT_RARITY_COLORS[trait.rarity] || '#0ea5e9';
                    return (
                      <span
                        key={index}
                        className={`
                          py-1.5 px-3 rounded-lg text-sm font-medium
                          transition-all duration-300 hover:scale-105
                          bg-gray-800 border border-cyan-400/20
                        `}
                        style={{ 
                          color: traitColor,
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
            </div>

            <hr className="border-t border-gray-700" />

            {/* Attribute Description - flex-grow-1 to fill remaining space */}
            <div className="flex-grow">
              <div className="h-full rounded-lg bg-gray-800/50 border border-cyan-400/20 p-4 overflow-y-auto">
                {selectedAttribute ? (
                  <p className="text-gray-300">{getAttributeDescription()}</p>
                ) : (
                  <p className="text-gray-400 italic">Click on any attribute above to see its detailed analysis</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImageAnalysis;
