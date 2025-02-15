import React, { createContext, useContext, useState } from 'react';

interface SuggestionsContextType {
    suggestions: string[];
    setSuggestions: (suggestions: string[]) => void;
}

const SuggestionsContext = createContext<SuggestionsContextType | undefined>(undefined);

export const SuggestionsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [suggestions, setSuggestions] = useState<string[]>([]);

    return (
        <SuggestionsContext.Provider value={{ suggestions, setSuggestions }}>
            {children}
        </SuggestionsContext.Provider>
    );
};

export const useSuggestions = () => {
    const context = useContext(SuggestionsContext);
    if (context === undefined) {
        throw new Error('useSuggestions must be used within a SuggestionsProvider');
    }
    return context;
}; 