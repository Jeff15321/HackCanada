import React, { createContext, useContext, useState } from 'react';
import { ChatMessageType } from '@/types/ChatMessageType';
import { useUser } from '../UserContext';
import { PostChatMessage } from '@/services/api';
import { useSuggestions } from './SuggestionsContext';

interface ChatContextType {
    message: string;
    setMessage: (message: string) => void;
    selectedFiles: File[];
    setSelectedFiles: (files: File[]) => void;
    handleChatSubmit: () => void;
    resetInputs: boolean;
    setResetInputs: (resetInputs: boolean) => void;
    selectedSuggestions: string[];
    setSelectedSuggestions: React.Dispatch<React.SetStateAction<string[]>>;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [message, setMessage] = useState('');
    const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
    const [resetInputs, setResetInputs] = useState(false);
    const [selectedSuggestions, setSelectedSuggestions] = useState<string[]>([]);
    const { user } = useUser();

    const handleChatSubmit = () => {
        if (!message && selectedFiles.length === 0) return;

        const chatMessage: ChatMessageType = {
            files: selectedFiles,
            message: message,
            date: new Date(),
            user_id: Number(user?.id),
            suggestions: selectedSuggestions
        };

        PostChatMessage(chatMessage);
        console.log(chatMessage);
        
        // Clear inputs
        setSelectedFiles([]);
        setMessage('');
        setResetInputs(true);
        setTimeout(() => setResetInputs(false), 100);
    };

    return (
        <ChatContext.Provider value={{
            message,
            setMessage,
            selectedFiles,
            setSelectedFiles,
            handleChatSubmit,
            resetInputs,
            setResetInputs,
            selectedSuggestions,
            setSelectedSuggestions
        }}>
            {children}
        </ChatContext.Provider>
    );
};

export const useChat = () => {
    const context = useContext(ChatContext);
    if (context === undefined) {
        throw new Error('useChat must be used within a ChatProvider');
    }
    return context;
}; 