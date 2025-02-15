import React, {useState} from 'react';
import { FaPlus, FaImage, FaBriefcase, FaMailBulk, FaPlane, FaPaperPlane } from 'react-icons/fa';

const SuggestionsChat: React.FC = () => {
    const [suggestions, useSuggestions] = useState([
        "Suggestion 1",
        "Suggestion 2222",
        "Sugge 3",
        "Suggestion 42",
        "Suggestion 5",
        "Suggestion 6",
        "Suggestion 7",
        "Suggestion 8",
        "Suggestion 9",
        "Suggestion 10"
    ]);
    return (
        <div className="flex flex-wrap gap-x-2 gap-y-1.5">
            {suggestions.map((suggestion, index) => (
                <button
                    key={index}
                    className="bg-white border border-gray-300 rounded-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                    {suggestion}
                </button>
            ))}
        </div>
    );
}

export default SuggestionsChat;