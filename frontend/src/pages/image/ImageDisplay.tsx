import React, { useState } from 'react';
import ImageDrop from '../../components/layout/ImageDrop';
import ImageAnalysis from '../../components/layout/ImageAnalysis';
import ImageLayout from '../../components/layout/ImageLayout';
import { newImage } from '../../services/api';
import { useModel } from '../../contexts/ModalContext';
import { useUser } from '../../contexts/UserContext';

const ImageDisplay = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const { model } = useModel();
  const { user } = useUser();

  const handleImageCapture = (file: File) => {
    setSelectedFile(file);
    setImageUrl(URL.createObjectURL(file));
  };

  const handleSubmit = async () => {
    try {
      if (!imageUrl || !user?.id) {
        throw new Error('Missing image or user ID');
      }
      
      await newImage(user.id, imageUrl);
      setIsAnalyzing(true);
    } catch (error) {
      console.error('Error submitting image:', error);
    }
  };

  return (
    <ImageLayout>
      {!isAnalyzing ? (
        <ImageDrop onImageCapture={handleImageCapture} onSubmit={handleSubmit} />
      ) : (
        <ImageAnalysis imageUrl={imageUrl!} />
      )}
    </ImageLayout>
  );
};

export default ImageDisplay; 