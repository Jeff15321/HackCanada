import React from 'react';
import WalletLogin from '../auth/WalletLogin';
import ImageDrop from '../layout/FlowerViews/ImageDrop';
import { newImage } from '@/services/api';
import { useUser } from '@/contexts/UserContext';
import { useModel } from '@/contexts/ModelContext';
import { useImage } from '@/contexts/ImageContext';
import router from 'next/router';

interface FlowerParameters {
  colorVibrancy: {
    score: number;
    explanation: string;
  };
  leafAreaIndex: {
    score: number;
    explanation: string;
  };
  wilting: {
    score: number;
    explanation: string;
  };
  spotting: {
    score: number;
    explanation: string;
  };
  symmetry: {
    score: number;
    explanation: string;
  };
}

interface FlowerModel {
  glbFileUrl: string;
  parameters: FlowerParameters;
  name: string;
  walletID: string;
  price: number;
  imageUrl: string;
  special: { attribute: string; rarity: number; }[];
}

const Profile = () => {
  const { user } = useUser();
  const { selectedFile, imageUrl, isAnalyzing, setIsAnalyzing } = useImage();
  const { model, setModel } = useModel();

  const handleSubmit = async (flowerName: string) => {
    try {
      if (!selectedFile || !user?.id || !imageUrl) {
        throw new Error('Missing required data');
      }

      const randomAttributes = {
        health: Math.floor(Math.random() * 100),
        growth: Math.floor(Math.random() * 100),
        waterLevel: Math.floor(Math.random() * 100),
        sunlight: Math.floor(Math.random() * 100)
      };

      const response = await newImage(
        user.id, 
        imageUrl, 
        flowerName,
        model?.description, 
        model?.glbFileUrl,
        selectedFile, 
        randomAttributes
      );

      const newModel: FlowerModel = {
        ...response,
        name: flowerName,
        imageUrl: response.glbFileUrl || '',
        special: response.special || []
      };

      setModel(newModel);
      return newModel;
    } catch (error) {
      console.error('Error submitting image:', error);
      throw error;
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