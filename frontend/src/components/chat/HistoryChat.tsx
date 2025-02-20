import React, { useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { HistoryChatType } from '@/types/ChatMessageType';

interface HistoryChatProps {
    historyChat: HistoryChatType[];
}

const HistoryChat: React.FC<HistoryChatProps> = ({ historyChat }) => {
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [historyChat]);

    // TODO: can you play around with the markdown style to reduce the gap between bolded points?
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
                                    <ReactMarkdown>
                                        {typeof chat.message === 'string' ? chat.message : JSON.stringify(chat.message)}
                                    </ReactMarkdown>
                                </div>
                            )}
                        </div>
                    </div>
                ))}
                <hr className="border-gray-200 my-4" />
                <div ref={messagesEndRef} />
            </div>
        </div>
    );
};

export default HistoryChat;