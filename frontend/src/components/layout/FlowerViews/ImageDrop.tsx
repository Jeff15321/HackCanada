import React, { useState, useRef } from 'react';
import { IconButton } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import DeleteIcon from '@mui/icons-material/Delete';
import { useImage } from '../../../contexts/ImageContext';

interface ImageDropProps {
  onSubmit: () => void;
}

const ImageDrop: React.FC<ImageDropProps> = ({ onSubmit }) => {
  const [image, setImage] = useState<string | null>(null);
  const [isAnimating, setIsAnimating] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [flowerName, setFlowerName] = useState('');
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
      <div className="flex gap-24 items-center">
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

        </div>

        {/* Right side - Controls */}
        <div className="w-96 flex flex-col gap-16">
          <input
            type="file"
            accept="image/*"
            hidden
            ref={fileInputRef}
            onChange={(e) => e.target.files?.[0] && handleImageSelect(e.target.files[0])}
          />
             {/* Epic Name Input */}
          <div className="space-y-3 relative group">
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
                  bg-white/80 backdrop-blur-sm
                  border-2 border-transparent
                  group-hover:border-purple-300
                  focus:border-purple-500
                  shadow-[0_0_15px_rgba(168,85,247,0.15)]
                  group-hover:shadow-[0_0_20px_rgba(168,85,247,0.25)]
                  focus:shadow-[0_0_25px_rgba(168,85,247,0.35)]
                  transition-all duration-300
                  outline-none
                  placeholder:text-gray-400"
              />
              <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-purple-500/20 to-cyan-500/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
            </div>
          </div>
          
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
                {isAnimating ? 'SUBMITTING...' : 'SUBMIT'}
              </span>
            </span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ImageDrop;
