import React, { useEffect, useState } from 'react';
import ImageDrop from './ImageDrop';
import ImageAnalysis from './ImageAnalysis';
import { newImage } from '../../../services/api';
import { useModel } from '../../../contexts/ModelContext';
import { useUser } from '../../../contexts/UserContext';
import { useImage } from '../../../contexts/ImageContext';
import Navigation from '../Navigation';
import Marketplace from '../../sections/Marketplace';
import Collection from '../../sections/Collection';
import Profile from '../../sections/Profile';
import FlowerView from '../FlowerView';
import BackgroundWrapper from './BackgroundWrapper';

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

type Tab = 'marketplace' | 'collection' | 'profile';

const ImageDisplay = () => {
  const { selectedFile, imageUrl, isAnalyzing, setIsAnalyzing } = useImage();
  const { model, setModel } = useModel();
  const { user } = useUser();
  const [activeTab, setActiveTab] = useState<Tab>('marketplace');

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
    <BackgroundWrapper>
      <div className="h-screen flex">
        <div className="flex-1 overflow-y-auto">
          {/* Navigation at the top */}
          <div className="fixed top-[1rem] left-0 right-0 z-10 flex-none">
            <Navigation activeTab={activeTab} onTabChange={setActiveTab} />
          </div>

          {/* Main content area */}
          <div className="flex-grow relative w-full max-w-7xl mx-auto">
            {/* Show content based on active tab */}
            {/* {activeTab === 'marketplace' && !isAnalyzing && <ImageDrop onSubmit={handleSubmit} />}
            {activeTab === 'marketplace' && isAnalyzing && <FlowerView />} */}
            {activeTab === 'marketplace' && <Marketplace />}
            {activeTab === 'collection' && <Collection />}
            {activeTab === 'profile' && <Profile />}
          </div>
        </div>
      </div>
    </BackgroundWrapper>
  );
};

export default ImageDisplay; 