import React, { useState, useRef, useEffect } from 'react';
import { IconButton } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import DeleteIcon from '@mui/icons-material/Delete';
import { useImage } from '@/contexts/ImageContext';
import styles from '@/styles/CoinFlip.module.css';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import router from 'next/router';
import { calculateRarity, RARITY_COLORS } from './ImageAnalysis';
import { Model } from '@/types/ModelType';
import { runPipelineViaBackend } from '@/services/api';

interface ImageDropProps {
  onSubmit: (flowerName: string) => Promise<Model>;
}

type RarityTextMap = {
  [key: number]: { text: string; color: string; }
};

const ImageDrop: React.FC<ImageDropProps> = ({ onSubmit }) => {
  const [image, setImage] = useState<string | null>(null);
  const [isAnimating, setIsAnimating] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [flowerName, setFlowerName] = useState('');
  const { setSelectedFile, setImageUrl } = useImage();
  const [isHeads, setIsHeads] = useState(true);
  const [colorCounter, setColorCounter] = useState(0);
  const [isFlipping, setIsFlipping] = useState(false);
  const [isCoinMovingRight, setIsCoinMovingRight] = useState(false);
  const [showTrailText, setShowTrailText] = useState(false);
  const [isFadingOut, setIsFadingOut] = useState(false);
  const [rarity, setRarity] = useState(0);
  const [particles, setParticles] = useState<Array<{ id: number; x: number; y: number }>>([]);
  const colors = [
    { bg: 'rgba(75, 85, 99, 0.2)', border: 'rgb(156, 163, 175)' },     // Gray
    { bg: 'rgba(59, 130, 246, 0.2)', border: 'rgb(96, 165, 250)' },    // Blue
    { bg: 'rgba(249, 115, 22, 0.2)', border: 'rgb(251, 146, 60)' },    // Orange
    { bg: 'rgba(147, 51, 234, 0.2)', border: 'rgb(192, 132, 252)' },   // Purple
    { bg: 'rgba(234, 179, 8, 0.2)', border: 'rgb(250, 204, 21)' },     // Yellow
  ];

  const handleFileDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      handleImageSelect(file);
    }
  };

  const handleImageSelect = (file: File) => {
    setSelectedFile(file);
    if (file) {
      const url = URL.createObjectURL(file);
      setImageUrl(url);
      const reader = new FileReader();
      reader.onload = () => setImage(reader.result as string);
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async () => {
    setIsAnimating(true);
    try {
      const response = await onSubmit(flowerName);
      
      // Run the pipeline after model creation
      try {
        const pipelineResponse = await runPipelineViaBackend(response);
        console.log('Pipeline Response:', {
          mint: pipelineResponse.mint,
          ownerTokens: pipelineResponse.ownerTokens
        });
      } catch (pipelineError: any) {  // Type as 'any' to access response property
        console.error('Pipeline error:', pipelineError?.response?.data || pipelineError);
        // Continue with the flow even if pipeline fails
      }
      
      setIsAnimating(false);
      
      // Calculate rarity from model parameters
      const stats = {
        colorVibrancy: response.parameters.colorVibrancy,
        leafAreaIndex: response.parameters.leafAreaIndex,
        wilting: response.parameters.wilting,
        spotting: response.parameters.spotting,
        symmetry: response.parameters.symmetry
      };
      
      // Map rarity levels to number of flips
      const rarityToFlips = {
        'Legendary': 5,
        'Epic': 4,
        'Rare': 3,
        'Common': 2,
        'Garbage': 1
      };

      const rarityLevel = calculateRarity(stats);
      setRarity(rarityToFlips[rarityLevel]);
      setIsFlipping(true);
    } catch (error) {
      console.error('Submit error:', error);
      setIsAnimating(false);
    }
  };

  const clearImage = (e: React.MouseEvent) => {
    e.stopPropagation();
    setImage(null);
    setSelectedFile(null);
    setImageUrl(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const flipCoin = (e: React.MouseEvent) => {
    if (!isFlipping) {
      fileInputRef.current?.click();
      return;
    }
    
    setIsHeads(prev => !prev);
    const circle = document.querySelector(`.${styles.coin}`) as HTMLElement;
    setTimeout(() => {
      if (circle) {
        const nextColor = colors[colorCounter];
        circle.style.backgroundColor = nextColor.bg;
        circle.style.borderColor = nextColor.border;
        createParticles(e, nextColor.border);
        setColorCounter((prev) => (prev + 1) % 5);
        if (colorCounter >= rarity - 2) {
          const clickMeContainer = document.querySelector(`.${styles.fadeInDelayed}`) as HTMLElement;
        
          if (clickMeContainer) {
            clickMeContainer.style.animation = `${styles.properFadeOut} 1s forwards`;
          }
  
          const clickMeElement = document.querySelector(`.${styles.fadeInDelayed}`) as HTMLElement;
          if (clickMeElement) {
            clickMeElement.style.animation = `${styles.properFadeOut} 0.5s forwards`;
          }
          
          // Wait for fade-out to complete before moving coin
          setTimeout(() => {
            setIsCoinMovingRight(true);
          }, 500);
        }
      }
    }, 300);
  };

  const createParticles = (e: React.MouseEvent, color: string) => {
    const newParticles = Array.from({ length: 8 }).map(() => ({
      id: Math.random(),
      x: e.clientX - 10, // Center on click
      y: e.clientY - 10
    }));
    setParticles(newParticles);
    setTimeout(() => setParticles([]), 500);
  };

  useEffect(() => {
    if (isCoinMovingRight) {
      setShowTrailText(true);
      setTimeout(() => {
        setIsFadingOut(true);  // Trigger fade out
        setTimeout(() => {
          router.push('/image/163426555534756543783');
        }, 800);
        setTimeout(() => {
          setIsFlipping(false);
          setShowTrailText(false);
          setIsFadingOut(false);

        }, 1000);
      }, 2000);
    }
  }, [isCoinMovingRight]);

  const overlayStyles = isFlipping ? {
    position: 'fixed',
    inset: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
    opacity: isFadingOut ? 0 : 1,
    transition: 'opacity 1s ease-in-out',
    zIndex: 40,
  } as const : {};

  // Add rarity text mapping
  const rarityText: RarityTextMap = {
    5: { text: "LEGENDARY!", color: RARITY_COLORS.Legendary },
    4: { text: "EPIC!", color: RARITY_COLORS.Epic },
    3: { text: "RARE!", color: RARITY_COLORS.Rare },
    2: { text: "COMMON!", color: RARITY_COLORS.Common },
    1: { text: "GARBAGE!", color: RARITY_COLORS.Garbage }
  };

  return (
    <div className="container mx-auto max-w-6xl h-screen flex items-center justify-center">
      {showTrailText && (
        <div 
          className={`${styles.textTrail} ${isFadingOut ? styles.fadeOut : ''}`}
          style={{
            position: 'fixed',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            color: rarityText[rarity]?.color || '#fff'
          }}
        >
          <p className="text-8xl font-bold">{rarityText[rarity]?.text || 'Epic!'}</p>
        </div>
      )}
      
      {isFlipping && (
        <>
          <div style={overlayStyles} />
          <div className={`
            fixed right-32 top-1/2 -translate-y-1/2 z-50 
            flex items-center gap-4 text-white animate-pulse
            ${styles.fadeInDelayed}
          `}>
            <ArrowBackIcon className="text-8xl" />

            <p className="text-8xl font-bold">Click me!</p>
          </div>
        </>
      )}
      <div className="flex gap-24 items-center justify-center w-full">
        {/* Left side - Summon Circle */}
        <div className={`w-1/2 max-w-xl ${styles.coinContainer} relative z-50`}>
          <div 
            className={`
              aspect-square w-full
              border-[8px] border-purple-500
              rounded-full
              flex items-center justify-center
              bg-purple-900/20 backdrop-blur-sm
              cursor-pointer
              overflow-hidden
              shadow-[0_0_50px_rgba(168,85,247,0.5)]
              transition-all duration-300
              ${styles.coin}
              ${isFlipping ? (isHeads ? styles.flipHeads : styles.flipTails) : ''}
              ${isCoinMovingRight ? styles.moveRight : ''}
            `}
            style={{
              borderColor: isFlipping ? colors[colorCounter].border : 'rgb(168,85,247)',
              boxShadow: isFlipping 
                ? `0 0 50px ${colors[colorCounter].border}80` 
                : '0 0 50px rgba(168,85,247,0.5)'
            }}
            onDrop={handleFileDrop}
            onDragOver={(e) => e.preventDefault()}
            onClick={flipCoin}
          >
            {!image ? (
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <CloudUploadIcon className="text-6xl text-white/50 mb-4 animate-bounce" />
                <p className="text-3xl font-semibold text-white/90">
                  Drop your flower here
                </p>
      
              </div>
            ) : (
              <div className="relative w-full h-full flex items-center justify-center">
                <img
                  src={image}
                  alt="Preview"
                  className={`
                    w-full h-full object-cover
                    ${isAnimating ? 'animate-pulse' : ''}
                  `}
                />
            
              </div>
            )}
          </div>

          <div className={styles.particleContainer}>
            {particles.map(particle => (
              <div
                key={particle.id}
                className={styles.particle}
                style={{
                  left: '50%',
                  top: '50%',
                  backgroundColor: colors[colorCounter].border,
                  boxShadow: `0 0 20px ${colors[colorCounter].border}`,
                  '--x': particle.x,
                  '--y': particle.y
                } as any}
              />
            ))}
          </div>
        </div>

        {/* Right side - Upload Controls */}
        <div className="w-1/2 max-w-xl">
          <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-8 border border-cyan-400/20">
            <input
              type="file"
              ref={fileInputRef}
              className="hidden"
              onChange={(e) => e.target.files?.[0] && handleImageSelect(e.target.files[0])}
              accept="image/*"
            />

            {/* Name Input */}
            <div className="space-y-3 relative group mb-8">
              <label className="block text-xl font-bold bg-gradient-to-r from-purple-600 to-cyan-600 bg-clip-text text-transparent">
                Name Your Flower
              </label>
              <div className="relative">
                <input
                  type="text"
                  value={flowerName}
                  onChange={(e) => setFlowerName(e.target.value)}
                  placeholder="Enter flower name"
                  className="w-full px-6 py-4 rounded-xl text-lg
                    bg-white/5 backdrop-blur-sm text-white
                    border-2 border-transparent
                    group-hover:border-cyan-400/20
                    focus:border-cyan-400/40
                    transition-all duration-300
                    outline-none
                    placeholder:text-gray-400"
                />
              </div>
            </div>

            {/* Buttons */}
            <button 
              className={`
                group relative w-full py-7 rounded-lg text-2xl font-black
                transition-all duration-300 transform
                bg-gradient-to-r from-cyan-900 to-cyan-700
                text-white hover:scale-105 backdrop-blur-sm font-game
                ${isAnimating && 'opacity-50 cursor-not-allowed hover:scale-100'}
                before:absolute before:inset-0
                before:bg-gradient-to-r before:from-transparent before:via-cyan-400 before:to-transparent
                before:opacity-0 before:transition-opacity before:duration-500
                hover:before:opacity-20
                after:absolute after:inset-[2px]
                after:bg-gradient-to-r after:from-cyan-900 after:to-cyan-700
                after:rounded-[4px] after:-z-10
              `}
              onClick={() => fileInputRef.current?.click()}
              disabled={isAnimating}
            >
              <span className="relative z-10 inline-flex items-center justify-center w-full">
                <span className="bg-gradient-to-r from-cyan-200 to-cyan-400 bg-clip-text text-transparent">
                  UPLOAD FLOWER
                </span>
              </span>
            </button>
            
            <button 
              className={`
                group relative w-full py-7 mt-4 rounded-lg text-2xl font-black
                transition-all duration-300 transform font-game
                ${!image 
                  ? 'bg-gray-800 text-gray-500 cursor-not-allowed' 
                  : `
                    bg-gradient-to-r from-purple-900 to-purple-700
                    text-white hover:scale-105
                    before:absolute before:inset-0
                    before:bg-gradient-to-r before:from-transparent before:via-purple-400 before:to-transparent
                    before:opacity-0 before:transition-opacity before:duration-500
                    hover:before:opacity-20
                    after:absolute after:inset-[2px]
                    after:bg-gradient-to-r after:from-purple-900 after:to-purple-700
                    after:rounded-[4px] after:-z-10
                  `
                }
              `}
              disabled={!image || isAnimating}
              onClick={
                handleSubmit
              }

            >
              <span className="relative z-10 inline-flex items-center justify-center w-full">
                <span className={`
                  ${!image 
                    ? 'text-gray-500'
                    : 'bg-gradient-to-r from-purple-200 to-purple-400 bg-clip-text text-transparent'
                  }
                `}>
                  {isAnimating ? 'SUBMITTING...' : 'SUBMIT'}
                </span>
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImageDrop;
