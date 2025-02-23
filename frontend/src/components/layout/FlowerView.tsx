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
      <div className="h-[95vh] w-[90vw] ml-[5vw]">
        <div className="h-[100%] mx-auto py-6">
          <div className="flex flex-row gap-8">
            {/* Left side - Image Analysis */}
            <div className="flex-1">
                <ImageAnalysis />
            </div>

            {/* Right side - Payment and Details */}
            <div className="w-[20vw]">
               <Payment /> 
            </div>
          </div>
        </div>
      </div>
    </BackgroundWrapper>
  );
};

export default FlowerView;