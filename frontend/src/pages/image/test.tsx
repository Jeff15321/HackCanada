import React from 'react';
import ImageDisplay from '../../components/layout/FlowerViews/ImageDisplay';
import Payment from '../../components/layout/FlowerViews/Payment';

const testPage = () => {
  return (
    <div className="h-full border-2 border-red-500">
      <div className="flex min-h-[calc(100vh-6rem)]">
        <div className="flex-2 border-2 border-blue-500">
            

        </div>
        <div className="flex-1 border-2 border-yellow-500">
            <Payment />
        </div>
      </div>
    </div>
  );
};

export default testPage; 