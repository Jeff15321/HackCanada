import React from 'react';
import ReactMarkdown from 'react-markdown';

interface ChatMessageProps {
    content: string;
    isUser: boolean;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ content, isUser }) => {
    return (
        <div className={`py-6 px-4 ${isUser ? 'bg-white' : 'bg-gray-50'}`}>
            <div className="max-w-3xl mx-auto flex gap-4">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center 
                    ${isUser ? 'bg-blue-500' : 'bg-gray-700'}`}>
                    {isUser ? '👤' : '🤖'}
                </div>
                <div className="flex-1 prose max-w-none">
                    <ReactMarkdown>{content}</ReactMarkdown>
                </div>
            </div>
        </div>
    );
};

export default ChatMessage; 