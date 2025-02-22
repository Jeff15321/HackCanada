import React, { useState, useRef } from 'react';
import { IconButton } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import DeleteIcon from '@mui/icons-material/Delete';
import { useImage } from '../../contexts/ImageContext';

interface ImageDropProps {
  onSubmit: () => void;
}

const ImageDrop: React.FC<ImageDropProps> = ({ onSubmit }) => {
  const [image, setImage] = useState<string | null>(null);
  const [isAnimating, setIsAnimating] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { setSelectedFile, setImageUrl } = useImage();

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

  const handleSubmit = () => {
    setIsAnimating(true);
    setTimeout(() => {
      setIsAnimating(false);
      onSubmit();
    }, 2000);
  };

  const clearImage = (e: React.MouseEvent) => {
    e.stopPropagation();
    setImage(null);
    setSelectedFile(null);
    setImageUrl(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="container mx-auto max-w-6xl p-6">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400 mb-2 font-game">
          SUMMON YOUR CRYPTO FLOWER
        </h1>
      </div>

      <div className="flex gap-12 items-center">
        {/* Left side - Summon Circle */}
        <div className="flex-1 relative">
          <div 
            className={`
              aspect-square w-full max-w-xl
              border-4 border-purple-500/50 rounded-full
              flex items-center justify-center
              bg-purple-900/20 backdrop-blur-sm
              transition-all duration-300 cursor-pointer
              overflow-hidden
              ${isAnimating ? 'animate-spin' : 'hover:border-purple-400/80'}
              ${image ? 'border-emerald-500/50' : ''}
            `}
            onDrop={handleFileDrop}
            onDragOver={(e) => e.preventDefault()}
            onClick={() => fileInputRef.current?.click()}
          >
            {!image ? (
              <div className="text-center p-8">
                <CloudUploadIcon className="text-6xl text-white/50 mb-4 animate-bounce" />
                <p className="text-xl font-semibold text-white/90">
                  Drop your flower here
                </p>
                <p className="text-sm text-white/70 mt-2">
                  to begin the summoning ritual
                </p>
              </div>
            ) : (
              <div className="relative w-full h-full flex items-center justify-center">
                <img
                  src={image}
                  alt="Preview"
                  className={`
                    max-w-full max-h-full object-contain
                    ${isAnimating ? 'animate-pulse' : ''}
                  `}
                />
                <IconButton
                  className="absolute top-4 right-4 bg-white/10 hover:bg-white/20"
                  onClick={clearImage}
                >
                  <DeleteIcon className="text-white/90" />
                </IconButton>
              </div>
            )}
          </div>

          {/* Mystic Effects */}
          <div className="absolute inset-0 pointer-events-none">
            <div className="absolute inset-0 bg-gradient-to-tr from-purple-500/20 to-emerald-500/20 rounded-full animate-pulse" />
          </div>
        </div>

        {/* Right side - Controls */}
        <div className="w-96 flex flex-col gap-8">
          <input
            type="file"
            accept="image/*"
            hidden
            ref={fileInputRef}
            onChange={(e) => e.target.files?.[0] && handleImageSelect(e.target.files[0])}
          />
          
          <button 
            className={`
              group relative w-full py-7 rounded-lg text-2xl font-black
              transition-all duration-300 transform
              bg-gradient-to-r from-cyan-900 to-cyan-700
              text-white
              hover:scale-105
              backdrop-blur-sm
              font-game
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
              group relative w-full py-7 rounded-lg text-2xl font-black
              transition-all duration-300 transform
              font-game
              ${!image 
                ? 'bg-gray-800 text-gray-500 cursor-not-allowed' 
                : `
                  bg-gradient-to-r from-purple-900 to-purple-700
                  text-white
                  hover:scale-105
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
            onClick={handleSubmit}
          >
            <span className="relative z-10 inline-flex items-center justify-center w-full">
              <span className={`
                ${!image 
                  ? 'text-gray-500'
                  : 'bg-gradient-to-r from-purple-200 to-purple-400 bg-clip-text text-transparent'
                }
              `}>
                {isAnimating ? 'SUMMONING...' : 'SUMMON'}
              </span>
            </span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ImageDrop;
