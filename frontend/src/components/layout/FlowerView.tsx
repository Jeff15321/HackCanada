import React from 'react';
import { Model } from '../../types/ModelType';
import ImageDisplay from './FlowerViews/ImageDisplay';
import Payment from './FlowerViews/Payment';  
import ImageAnalysis from './FlowerViews/ImageAnalysis';
import { useModel } from '../../contexts/ModelContext';

const FlowerView: React.FC = () => {
    const { model } = useModel();
    return (
        <div className="h-[80vh]">
            <div className="flex min-h-[calc(100vh-6rem)] gap-6 p-6">
                <div className="flex-2">
                    <ImageAnalysis />
                </div>
                <div className="flex-1">
                    <Payment value={1500} />
                </div>
            </div>
        </div>
    );
};

export default FlowerView;