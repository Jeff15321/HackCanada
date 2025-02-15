import React, { useEffect } from 'react';
import { useSuggestions } from '@/contexts/chat/SuggestionsContext';
import { useChat } from '@/contexts/chat/ChatContext';

const SuggestionsChat: React.FC = () => {
    const { suggestions } = useSuggestions();
    const { selectedSuggestions, setSelectedSuggestions } = useChat();

    const handleSuggestionClick = (suggestion: string) => {
        setSelectedSuggestions((prev: string[]) => {
            if (prev.includes(suggestion)) {
                return prev.filter((s: string) => s !== suggestion);
            }
            return [...prev, suggestion];
        });
    };

    return (
        <div className="flex flex-wrap gap-x-2 gap-y-1.5">
            {suggestions.slice(0, 10).map((suggestion, index) => (
                <button
                    key={index}
                    onClick={() => handleSuggestionClick(suggestion)}
                    className={`px-4 py-2 rounded-full text-sm 
                               transition-all duration-200 ease-in-out
                               ${selectedSuggestions.includes(suggestion) 
                                 ? 'bg-blue-400 border border-transparent text-white hover:bg-blue-500' 
                                 : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-100'
                               }`}
                >
                    {suggestion}
                </button>
            ))}
        </div>
    );
};

export default SuggestionsChat;