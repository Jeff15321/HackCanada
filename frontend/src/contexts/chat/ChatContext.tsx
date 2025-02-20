import React, { createContext, useContext, useState } from 'react';
import { ChatMessageType, SubTask } from '@/types/ChatMessageType';
import { useUser } from '../UserContext';
import { useSuggestions } from './SuggestionsContext';
import { LLMChatProcess, getSubTasks } from '@/services/api';
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
    isSubTaskWindowOpen: boolean;
    setIsSubTaskWindowOpen: (isSubTaskWindowOpen: boolean) => void;
    subTasks: SubTask[];
    setSubTasks: (subTasks: SubTask[]) => void;
    fetchSubTasks: () => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [message, setMessage] = useState('');
    const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
    const [resetInputs, setResetInputs] = useState(false);
    const [selectedSuggestions, setSelectedSuggestions] = useState<string[]>([]);
    const [isChatInputCentered, setIsChatInputCentered] = useState(true);
    const [subTasks, setSubTasks] = useState<SubTask[]>([]);
    const [isSubTaskWindowOpen, setIsSubTaskWindowOpen] = useState(false);

    const { user } = useUser();
    const { addMessage } = useChatHistory();

    
    // Fetch subtasks when window opens
    const fetchSubTasks = async () => {
        if (user) {
            try {
                console.log("Fetching subtasks");
                const tasks = await getSubTasks(user.id, "dummy_project_id", "");
                setSubTasks(tasks);
                console.log("Subtasks fetched:", tasks);
            } catch (error) {
                console.error('Error fetching subtasks:', error);
            }
        }
    };

    const handleChatSubmit = async () => {
        if (!message && selectedFiles.length === 0) return;

        // Store message for API call
        const messageToSend = message;

        // Update all states immediately
        setIsChatInputCentered(false);
        setMessage('');
        setSelectedFiles([]);
        setResetInputs(true);
        setIsSubTaskWindowOpen(true);
        
        // Add user message to history
        addMessage({
            message: messageToSend,
            is_user: true,
            file_name: '',
            date: new Date(),
            user_id: Number(user?.id)
        });
        

        try {
            const response = await LLMChatProcess(messageToSend);
            // Add AI response to history
            addMessage({
                message: response.merged_result_with_agent,
                is_user: false,
                file_name: '',
                date: new Date(),
                user_id: Number(user?.id)
            });

            const subTasksResponse = await getSubTasks(String(user?.id), response.project_id, messageToSend);
            setSubTasks(subTasksResponse);

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
            setIsChatInputCentered,
            isSubTaskWindowOpen,
            setIsSubTaskWindowOpen,
            subTasks,
            setSubTasks,
            fetchSubTasks
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