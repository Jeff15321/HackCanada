import React, { useEffect, useState } from 'react';
import { fetchAllModels } from '../../services/api';
import { Model } from '../../types/ModelType';
import ItemMenu from '../layout/FlowerViews/ItemMenu';
import { useUser } from '@/contexts/UserContext';

const Collection = () => {
  const [models, setModels] = useState<Model[]>([]);
  const { user } = useUser();

  useEffect(() => {
    const loadModels = async () => {
      const fetchedModels = await fetchAllModels();
      setModels(fetchedModels.filter((model) => model.id !== user?.id));
    };
    loadModels();
  }, []);

  return (
    <div className="h-screen flex flex-col">
      <div className="h-screen flex flex-col">
      <div className="flex-1 overflow-y-auto p-6">
        <div className="p-6 bg-white/80 backdrop-blur-sm border-b border-purple-100">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-cyan-600 bg-clip-text text-transparent">
            My Collection
          </h1>
        </div>
        <ItemMenu models={models} />
      </div>
    </div>
    </div>
  );
};

export default Collection; 