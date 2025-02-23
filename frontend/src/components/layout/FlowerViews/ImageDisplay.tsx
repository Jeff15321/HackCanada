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


type Tab = 'marketplace' | 'collection' | 'profile';

const ImageDisplay = () => {
  const { model, setModel } = useModel();
  const [activeTab, setActiveTab] = useState<Tab>('marketplace');

  useEffect(() => {
    console.log("model:", model);
  }, [model]);


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