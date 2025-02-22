import React, { useState, useEffect } from 'react';
import { Box, Paper, Typography, Divider, Chip } from '@mui/material';
import { keyframes } from '@emotion/react';
import LocalFloristIcon from '@mui/icons-material/LocalFlorist';
import OpacityIcon from '@mui/icons-material/Opacity';
import WbSunnyIcon from '@mui/icons-material/WbSunny';
import TimelapseIcon from '@mui/icons-material/Timelapse';

interface ImageAnalysisProps {
  imageUrl: string;
}

// Animation keyframes
const slideRight = keyframes`
  from {
    width: 0%;
  }
  to {
    width: var(--target-width);
  }
`;

type Rarity = 'Garbage' | 'Common' | 'Rare' | 'Epic' | 'Legendary';

const RARITY_COLORS = {
  Garbage: '#808080',  // gray
  Common: '#3498db',   // blue
  Rare: '#e67e22',     // orange
  Epic: '#9b59b6',     // purple
  Legendary: '#f1c40f' // gold
};

const RARITY_BACKGROUNDS = {
  Garbage: 'linear-gradient(45deg, rgba(128, 128, 128, 0.1) 0%, rgba(128, 128, 128, 0.2) 100%)',
  Common: 'linear-gradient(45deg, rgba(52, 152, 219, 0.1) 0%, rgba(52, 152, 219, 0.2) 100%)',
  Rare: 'linear-gradient(45deg, rgba(230, 126, 34, 0.1) 0%, rgba(230, 126, 34, 0.2) 100%)',
  Epic: 'linear-gradient(45deg, rgba(155, 89, 182, 0.1) 0%, rgba(155, 89, 182, 0.2) 100%)',
  Legendary: 'linear-gradient(45deg, rgba(241, 196, 15, 0.1) 0%, rgba(241, 196, 15, 0.3) 100%)'
};

const calculateRarity = (stats: { health: number; waterLevel: number; sunlight: number; growth: number }): Rarity => {
  const average = (stats.health + stats.waterLevel + stats.sunlight + stats.growth) / 4;
  
  // Equal 20% chance for each rarity
  if (average >= 55) return 'Legendary';    // Top 20%
  if (average >= 45) return 'Epic';         // Next 20%
  if (average >= 30) return 'Rare';         // Next 20%
  if (average >= 20) return 'Common';       // Next 20%
  return 'Garbage';                         // Bottom 20%
};

const generateRandomStats = () => {
  // Generate stats with a normal distribution centered around 80
  const generateStat = () => {
    let stat = 0;
    // Generate 3 random numbers and take the average for a more normal distribution
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

const AnimatedStat: React.FC<{ value: number; label: string; color: string }> = ({ 
  value, 
  label,
  color 
}) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const duration = 1500; // Animation duration in ms
    const steps = 60; // Number of steps
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
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
      <Box sx={{ flex: 1 }}>
        <Typography variant="body2" color="text.secondary">{label}</Typography>
        <Box sx={{ 
          width: '100%', 
          height: 8, 
          bgcolor: `${color}20`,
          borderRadius: 4,
          overflow: 'hidden'
        }}>
          <Box sx={{ 
            '--target-width': `${value}%`,
            width: `${value}%`,
            height: '100%',
            bgcolor: color,
            animation: `${slideRight} 1.5s ease-out`,
            transformOrigin: 'left',
          }} />
        </Box>
      </Box>
      <Typography variant="body1" fontWeight="bold" sx={{ 
        minWidth: '3rem',
        color: color
      }}>
        {count}%
      </Typography>
    </Box>
  );
};

const ImageAnalysis: React.FC<ImageAnalysisProps> = ({ imageUrl }) => {
  // Generate random stats and calculate rarity
  const stats = generateRandomStats();
  const rarity = calculateRarity(stats);
  const rarityColor = RARITY_COLORS[rarity];
  
  const flowerData = {
    name: "Crypto Rose",
    rarity: rarity,
    health: stats.health,
    growth: stats.growth,
    waterLevel: stats.waterLevel,
    sunlight: stats.sunlight,
    traits: ["Fast Growing", "Rare Color", "High Yield"],
    status: stats.health > 70 ? "Thriving" : "Struggling",
  };

  return (
    <Paper
      elevation={24}
      sx={{
        width: '100%',
        maxWidth: 1200,
        borderRadius: 4,
        overflow: 'hidden',
        background: 'rgba(255, 255, 255, 0.9)',
        backdropFilter: 'blur(10px)',
        border: `1px solid ${rarityColor}`,
        position: 'relative',
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: RARITY_BACKGROUNDS[rarity],
          pointerEvents: 'none',
        }
      }}
    >
      <Box
        sx={{
          display: 'flex',
          flexDirection: { xs: 'column', md: 'row' },
          minHeight: 600,
        }}
      >
        {/* Left Side - Image Display */}
        <Box
          sx={{
            flex: '1.2',
            p: 4,
            borderRight: { xs: 'none', md: '1px solid rgba(46, 20, 55, 0.1)' },
            borderBottom: { xs: '1px solid rgba(46, 20, 55, 0.1)', md: 'none' },
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Box
            sx={{
              width: '100%',
              height: '100%',
              borderRadius: 3,
              overflow: 'hidden',
              boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
              position: 'relative',
              '&::after': {
                content: '""',
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                boxShadow: 'inset 0 0 100px rgba(27, 153, 139, 0.2)',
                pointerEvents: 'none',
              }
            }}
          >
            <img
              src={imageUrl}
              alt="Analyzed Flower"
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'contain',
              }}
            />
          </Box>
        </Box>

        {/* Right Side - Analysis */}
        <Box
          sx={{
            flex: '1',
            p: 4,
            display: 'flex',
            flexDirection: 'column',
            gap: 3,
          }}
        >
          <Box>
            <Typography variant="h4" fontWeight="bold" color="#2E1437">
              {flowerData.name}
            </Typography>
            <Chip
              label={flowerData.rarity}
              sx={{
                mt: 1,
                backgroundColor: rarityColor,
                color: 'white',
                fontWeight: 'bold',
                padding: '8px 16px',
                height: 32,
                fontSize: '1rem',
                border: rarity === 'Legendary' ? '1px solid rgba(255,255,255,0.5)' : 'none',
                boxShadow: rarity === 'Legendary' ? '0 0 10px rgba(241, 196, 15, 0.5)' : 'none',
                animation: rarity === 'Legendary' ? 'pulse 2s infinite' : 'none',
                '@keyframes pulse': {
                  '0%': {
                    boxShadow: '0 0 0 0 rgba(241, 196, 15, 0.4)',
                  },
                  '70%': {
                    boxShadow: '0 0 0 10px rgba(241, 196, 15, 0)',
                  },
                  '100%': {
                    boxShadow: '0 0 0 0 rgba(241, 196, 15, 0)',
                  },
                },
              }}
            />
          </Box>

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <LocalFloristIcon sx={{ color: flowerData.status === 'Thriving' ? '#1B998B' : '#ff9800' }} />
            <Typography variant="h6" color={flowerData.status === 'Thriving' ? '#1B998B' : '#ff9800'}>
              Status: {flowerData.status}
            </Typography>
          </Box>

          <Divider sx={{ borderColor: 'rgba(46, 20, 55, 0.1)' }} />

          {/* Stats with Animation */}
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Typography variant="h6" color="#2E1437" gutterBottom>
              Vital Statistics
            </Typography>
            
            <AnimatedStat 
              value={flowerData.health} 
              label="Health" 
              color={rarityColor}
            />
            
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <OpacityIcon sx={{ color: '#1B998B' }} />
              <AnimatedStat 
                value={flowerData.waterLevel} 
                label="Water Level" 
                color={rarityColor}
              />
            </Box>

            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <WbSunnyIcon sx={{ color: '#1B998B' }} />
              <AnimatedStat 
                value={flowerData.sunlight} 
                label="Sunlight" 
                color={rarityColor}
              />
            </Box>

            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <TimelapseIcon sx={{ color: '#1B998B' }} />
              <AnimatedStat 
                value={flowerData.growth} 
                label="Growth" 
                color={rarityColor}
              />
            </Box>
          </Box>

          <Divider sx={{ borderColor: 'rgba(46, 20, 55, 0.1)' }} />

          {/* Traits */}
          <Box>
            <Typography variant="h6" color="#2E1437" gutterBottom>
              Special Traits
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {flowerData.traits.map((trait, index) => (
                <Chip
                  key={index}
                  label={trait}
                  sx={{
                    backgroundColor: `${rarityColor}20`,
                    color: rarityColor,
                    '&:hover': {
                      backgroundColor: `${rarityColor}30`,
                    },
                    border: rarity === 'Legendary' ? `1px solid ${rarityColor}` : 'none',
                  }}
                />
              ))}
            </Box>
          </Box>
        </Box>
      </Box>
    </Paper>
  );
};

export default ImageAnalysis; 