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
      {!isAnalyzing ? (
        <ImageDrop onSubmit={handleSubmit} />
      ) : (
        <ImageAnalysis imageUrl={imageUrl!} />
      )}
    </ImageLayout>
  );
};

export default ImageDisplay; 