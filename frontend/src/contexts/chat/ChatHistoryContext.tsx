import React, { createContext, useContext, useState } from 'react';
import { HistoryChatType } from '@/types/ChatMessageType';

interface ChatHistoryContextType {
    chatHistory: HistoryChatType[];
    addMessage: (message: HistoryChatType) => void;
    clearHistory: () => void;
}

const ChatHistoryContext = createContext<ChatHistoryContextType | undefined>(undefined);

export const ChatHistoryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [chatHistory, setChatHistory] = useState<HistoryChatType[]>([]);

    const addMessage = (message: HistoryChatType) => {
        setChatHistory(prev => [...prev, message]);
    };

    const clearHistory = () => {
        setChatHistory([]);
    };

    return (
        <ChatHistoryContext.Provider value={{
            chatHistory,
            addMessage,
            clearHistory
        }}>
            {children}
        </ChatHistoryContext.Provider>
    );
};

export const useChatHistory = () => {
    const context = useContext(ChatHistoryContext);
    if (context === undefined) {
        throw new Error('useChatHistory must be used within a ChatHistoryProvider');
    }
    return context;
}; 