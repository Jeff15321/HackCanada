import React from 'react';
import { Model } from '../../types/ModelType';
import ImageDisplay from './FlowerViews/ImageDisplay';
import Payment from './FlowerViews/Payment';  
import ImageAnalysis from './FlowerViews/ImageAnalysis';
import { useModel } from '../../contexts/ModelContext';

const FlowerView: React.FC = () => {
    const { model } = useModel();
    return (
        <div className="h-screen bg-black">
            <ImageDisplay />
        </div>
    );
};

export default FlowerView;