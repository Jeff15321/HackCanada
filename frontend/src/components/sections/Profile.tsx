import React from 'react';
import WalletLogin from '../auth/WalletLogin';
import ImageDrop from '../layout/FlowerViews/ImageDrop';
import { newImage, runPipelineViaBackend } from '@/services/api';
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
  id: string;
  glbFileUrl: string;
  parameters: FlowerParameters;
  name: string;
  walletID: string;
  price: number;
  imageUrl: string;
  special: { attribute: string; rarity: number; }[];
}

interface Model {
  glbFileUrl: string;
  parameters: FlowerParameters;
  name: string;
  walletID: string;
  price: number;
  id: string;
  imageUrl: string;
  special: { attribute: string; rarity: number; }[];
}

const Profile = () => {
  const { user } = useUser();
  const { selectedFile, imageUrl, isAnalyzing, setIsAnalyzing } = useImage();
  const { model, setModel } = useModel();

  const handleSubmit = async (flowerName: string): Promise<Model> => {
    try {
      // Create a default Model that matches the expected type
      const defaultModel: Model = {
        glbFileUrl: "https://example.com/plant.glb",
        parameters: {
          colorVibrancy: { score: 95, explanation: "Vibrant green" },
          leafAreaIndex: { score: 85, explanation: "Good coverage" },
          wilting: { score: 90, explanation: "No wilting" },
          spotting: { score: 100, explanation: "No spots" },
          symmetry: { score: 88, explanation: "Good symmetry" }
        },
        name: flowerName || "TEE Plant #3",
        walletID: "hackcanada.testnet",
        price: 1000000000000000000000000,
        id: "14",
        imageUrl: "https://example.com/plant.glb",
        special: []
      };

      // Run the pipeline
      await runPipelineViaBackend(1);
      
      // Set the model in context
      setModel(defaultModel);
      
      return defaultModel;
    } catch (error) {
      console.error('Error in handleSubmit:', error);
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