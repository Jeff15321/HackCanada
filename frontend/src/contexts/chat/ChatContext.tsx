import React, { createContext, useContext, useState } from 'react';
import { ChatMessageType } from '@/types/ChatMessageType';
import { useUser } from '../UserContext';
import { PostChatMessage } from '@/services/api';
import { useSuggestions } from './SuggestionsContext';
import { testChatProcess } from '@/services/api';
import { useChatHistory } from './ChatHistoryContext';

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
    isChatInputCentered: boolean;
    setIsChatInputCentered: (isChatInputCentered: boolean) => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [message, setMessage] = useState('');
    const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
    const [resetInputs, setResetInputs] = useState(false);
    const [selectedSuggestions, setSelectedSuggestions] = useState<string[]>([]);
    const [isChatInputCentered, setIsChatInputCentered] = useState(true);
    const { user } = useUser();
    const { addMessage } = useChatHistory();

    const handleChatSubmit = async () => {
        if (!message && selectedFiles.length === 0) return;

        // Store message for API call
        const messageToSend = message;

        // Update all states immediately
        setIsChatInputCentered(false);
        setMessage('');
        setSelectedFiles([]);
        setResetInputs(true);
        
        // Add user message to history
        addMessage({
            message: messageToSend,
            is_user: true,
            file_name: '',
            date: new Date(),
            user_id: Number(user?.id)
        });

        try {
            const response = await testChatProcess(messageToSend);
            console.log("grr", response.merged_result_with_agent);
            // Add AI response to history
            addMessage({
                message: response.merged_result_with_agent,
                is_user: false,
                file_name: '',
                date: new Date(),
                user_id: Number(user?.id)
            });

            // Reset the resetInputs flag after a short delay
            setTimeout(() => setResetInputs(false), 100);

            return response;
        } catch (error) {
            console.error('Error processing message:', error);
        }
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
            setSelectedSuggestions,
            isChatInputCentered,
            setIsChatInputCentered
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