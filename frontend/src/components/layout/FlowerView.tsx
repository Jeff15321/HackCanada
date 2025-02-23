import React from 'react';
import Payment from './FlowerViews/Payment';  
import ImageAnalysis from './FlowerViews/ImageAnalysis';
import { useModel } from '../../contexts/ModelContext';
import BackgroundWrapper from './FlowerViews/BackgroundWrapper';
import { useRouter } from 'next/router';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

const FlowerView: React.FC = () => {
  const { model } = useModel();
  const router = useRouter();

  const handleBack = () => {
    router.back();
  };

  return (
    <BackgroundWrapper>
      <div className="min-h-screen w-[90vw] ml-[5vw]">
        <div className="container mx-auto py-6">
          <div className="flex lg:flex-row gap-8">
            {/* Left side - Image Analysis */}
            <div className="flex-1">
              <div className="bg-gray-800/30 backdrop-blur-sm rounded-xl border border-cyan-400/20 p-6">
                <ImageAnalysis />
              </div>
            </div>

            {/* Right side - Payment and Details */}
            <div className="w-[25vw]">
               <Payment value={1500} />
            </div>
          </div>
        </div>
      </div>
    </BackgroundWrapper>
  );
};

export default FlowerView;