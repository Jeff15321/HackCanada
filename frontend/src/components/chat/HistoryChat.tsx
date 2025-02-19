import { HistoryChatType } from '@/types/ChatMessageType';
import React from 'react';
import ReactMarkdown from 'react-markdown';

interface HistoryChatProps {
    historyChat: HistoryChatType[];
}

const HistoryChat: React.FC<HistoryChatProps> = ({ historyChat }) => {
    return (
        <div className='w-full h-full overflow-y-auto'>
            <div className='flex flex-col'>
                {historyChat.map((chat, index) => (
                    <div key={index}>
                        <hr className="border-gray-200 my-4" />
                        <div className={`px-8 py-2 ${chat.is_user ? 'text-right' : ''}`}>
                            {chat.is_user ? (
                                <div className="text-gray-800 break-words">
                                    {chat.message}
                                </div>
                            ) : (
                                <div className="prose break-words whitespace-pre-wrap max-w-full">
                                    <ReactMarkdown>{chat.message}</ReactMarkdown>
                                </div>
                            )}
                        </div>
                    </div>
                ))}
                <hr className="border-gray-200 my-4" />
            </div>
        </div>
    );
};

export default HistoryChat;