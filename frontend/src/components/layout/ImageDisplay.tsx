import React, { useEffect } from 'react';
import ImageDrop from './ImageDrop';
import ImageAnalysis from './ImageAnalysis';
import ImageLayout from './ImageLayout';
import { newImage } from '../../services/api';
import { useModel } from '../../contexts/ModelContext';
import { useUser } from '../../contexts/UserContext';
import { useImage } from '../../contexts/ImageContext';

interface GPTResponse {
  shape: {
    analysis: string;
    rating: string;
  };
  color: {
    analysis: string;
    rating: string;
  };
  health: {
    analysis: string;
    rating: string;
  };
  development: {
    analysis: string;
    rating: string;
  };
  attributes: {
    attribute: string;
    rarity: string;
  }[];
}

const ImageDisplay = () => {
  const { selectedFile, imageUrl, isAnalyzing, setIsAnalyzing } = useImage();
  const { model, setModel } = useModel();
  const { user } = useUser();

  useEffect(() => {
    console.log("model:", model);
  }, [model]);

  const handleSubmit = async () => {
    try {
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

      // Call the API and store the full response
      const response = await newImage(
        user.id, 
        imageUrl, 
        model?.name, 
        model?.description, 
        model?.imageUrl, 
        selectedFile, 
        randomAttributes
      );

      try {
        console.log("analysis:", response.api2_data.analysis);
        // Remove markdown code block markers and clean the string
        const cleanJsonString = response.api2_data.analysis
          .replace(/```json\n/, '')  // Remove opening markdown
          .replace(/```$/, '')       // Remove closing markdown
          .trim();                   // Remove extra whitespace
        
        const api2_data = JSON.parse(cleanJsonString) as GPTResponse;
        console.log("api2_data:", api2_data);
        
        // Update the model with the parsed data
        setModel({
          id: crypto.randomUUID(),
          name: model?.name || 'Default Name',
          description: cleanJsonString, // Store the cleaned JSON string
          imageUrl: imageUrl,
          image: selectedFile,
          threeDModel: null,
          attributes: {
            shape: Number(api2_data.shape.rating.replace('%', '')),
            color: Number(api2_data.color.rating.replace('%', '')),
            health: Number(api2_data.health.rating.replace('%', '')),
            development: Number(api2_data.development.rating.replace('%', '')),
            attributes: api2_data.attributes.map(attr => ({
              attribute: attr.attribute,
              rarity: Number(attr.rarity)
            })),
          }
        });

        // Move setIsAnalyzing after successful model update
        setIsAnalyzing(true);
      } catch (error) {
        console.error('Error parsing api2_data:', error);
      }
      
      // Log the full response
      console.log('Full API Response:', response);
      
    } catch (error) {
      console.error('Error submitting image:', error);
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