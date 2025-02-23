import React from 'react';
import WalletLogin from '../auth/WalletLogin';
import ImageDrop from '../layout/FlowerViews/ImageDrop';
import { newImage } from '@/services/api';
import { useUser } from '@/contexts/UserContext';
import { useModel } from '@/contexts/ModelContext';
import { useImage } from '@/contexts/ImageContext';
import router from 'next/router';

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

const Profile = () => {
  const { user } = useUser();
  const { selectedFile, imageUrl, isAnalyzing, setIsAnalyzing } = useImage();
  const { model, setModel } = useModel();

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
        router.push('/image/1');
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
    <div className="fixed inset-0">
      {/* Gradient Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-gray-900 via-gray-800 to-black" />
      
      {/* Cyber Grid */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(6,182,212,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(6,182,212,0.05)_1px,transparent_1px)] bg-[size:64px_64px]" />
      
      {/* Content */}
      <WalletLogin>
        <div className="relative min-h-screen w-full p-8">
          <ImageDrop onSubmit={handleSubmit} />
        </div>
      </WalletLogin>
    </div>
  );
};

export default Profile; 