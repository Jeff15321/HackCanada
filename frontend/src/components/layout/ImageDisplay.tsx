import React from 'react';
import ImageDrop from './ImageDrop';
import ImageAnalysis from './ImageAnalysis';
import ImageLayout from './ImageLayout';
import { newImage } from '../../services/api';
import { useModel } from '../../contexts/Model';
import { useUser } from '../../contexts/UserContext';
import { useImage } from '../../contexts/ImageContext';

const ImageDisplay = () => {
  const { selectedFile, imageUrl, isAnalyzing, setIsAnalyzing } = useImage();
  const { model, setModel } = useModel();
  const { user } = useUser();

  const handleSubmit = async () => {
    try {
      console.log("Submitting with file:", selectedFile);
      console.log("User:", user);
      console.log("Image URL:", imageUrl);

      if (!selectedFile) {
        throw new Error('Please select an image first');
      }
      
      if (!user?.id) {
        throw new Error('Please log in to submit an image');
      }

      if (!imageUrl) {
        throw new Error('Image URL not found');
      }

      const randomAttributes = {
        health: Math.floor(Math.random() * 100),
        growth: Math.floor(Math.random() * 100),
        waterLevel: Math.floor(Math.random() * 100),
        sunlight: Math.floor(Math.random() * 100)
      };

      setModel({
        id: crypto.randomUUID(),
        name: model?.name || 'Default Name',
        description: model?.description || 'Default Description',
        imageUrl: imageUrl,
        image: selectedFile,
        attributes: randomAttributes
      });
      
      await newImage(
        user.id, 
        imageUrl, 
        model?.name, 
        model?.description, 
        model?.imageUrl, 
        selectedFile, 
        randomAttributes
      );
      setIsAnalyzing(true);
    } catch (error) {
      console.error('Error submitting image:', error);
      // You might want to show this error to the user
      alert(error instanceof Error ? error.message : 'An error occurred');
    }
  };

  return (
    <ImageLayout>
      <div className="relative w-full max-w-7xl mx-auto">
        {/* Optional decorative elements */}
        <div className="absolute -top-20 -left-20 w-40 h-40 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
        <div className="absolute -bottom-20 -right-20 w-40 h-40 bg-emerald-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-40 h-40 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>

        {/* Main content */}
        <div className="relative backdrop-blur-sm">
          {!isAnalyzing ? (
            <ImageDrop onSubmit={handleSubmit} />
          ) : (
            <ImageAnalysis imageUrl={imageUrl!} />
          )}
        </div>
      </div>
    </ImageLayout>
  );
};

export default ImageDisplay; 