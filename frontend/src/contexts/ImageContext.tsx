import React, { createContext, useContext, useState } from 'react';

interface ImageContextType {
  selectedFile: File | null;
  setSelectedFile: (file: File | null) => void;
  imageUrl: string | null;
  setImageUrl: (url: string | null) => void;
  isAnalyzing: boolean;
  setIsAnalyzing: (analyzing: boolean) => void;
}

const ImageContext = createContext<ImageContextType | undefined>(undefined);

export const ImageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  return (
    <ImageContext.Provider 
      value={{
        selectedFile,
        setSelectedFile,
        imageUrl,
        setImageUrl,
        isAnalyzing,
        setIsAnalyzing,
      }}
    >
      {children}
    </ImageContext.Provider>
  );
};

export const useImage = () => {
  const context = useContext(ImageContext);
  if (context === undefined) {
    throw new Error('useImage must be used within an ImageProvider');
  }
  return context;
}; 