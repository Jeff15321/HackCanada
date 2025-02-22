import React, { createContext, useContext, useState } from 'react';
import { Model } from '../types/ModelType';

interface ModelContextType {
    model: Model | null;
    setModel: (model: Model | null) => void;
}

const ModelContext = createContext<ModelContextType | undefined>(undefined);

export const ModelProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [model, setModel] = useState<Model | null>(null);

    return (
        <ModelContext.Provider value={{ model, setModel }}>
            {children}
        </ModelContext.Provider>
    );
};

export const useModel = () => {
    const context = useContext(ModelContext);
    if (!context) {
        throw new Error('useModel must be used within a ModelProvider');
    }
    return context;
}; 