import React, { useState, useRef, useEffect } from 'react';
import InputChat from "@/components/chat/InputChat"
import ButtonsChat from "@/components/chat/ButtonsChat"
import SuggestionsChat from "@/components/chat/SuggestionsChat"
import { ChatProvider, useChat } from '@/contexts/chat/ChatContext';
import { SuggestionsProvider } from '@/contexts/chat/SuggestionsContext';
import HistoryChat from '../chat/HistoryChat';
import { HistoryChatType } from '@/types/ChatMessageType'
import { ChatHistoryProvider, useChatHistory } from '@/contexts/chat/ChatHistoryContext';

const ChatContent: React.FC = () => {
    const { isChatInputCentered } = useChat();
    const { chatHistory } = useChatHistory();
    const [isProfessionOpen, setIsProfessionOpen] = useState(false);
    const [isChatInputOpen, setIsChatInputOpen] = useState(true);
    const inputRef = useRef<HTMLDivElement>(null);
    const [inputHeight, setInputHeight] = useState('0px');

    // Update height when input container changes
    useEffect(() => {
        const updateHeight = () => {
            if (inputRef.current) {
                setInputHeight(`${inputRef.current.offsetHeight}px`);
            }
        };

        // Initial update
        updateHeight();

        // Create observer
        const resizeObserver = new ResizeObserver(updateHeight);
        if (inputRef.current) {
            resizeObserver.observe(inputRef.current);
        }

        // Cleanup
        return () => {
            if (inputRef.current) {
                resizeObserver.unobserve(inputRef.current);
            }
        };
    }, [isProfessionOpen]); // Re-run when suggestions are toggled

    return (
        <div className="relative w-full h-full bg-gray-100">
            {/* Chat History */}
            <div className={`absolute inset-x-[10%] top-0 
                ${isChatInputCentered ? 'hidden' : 'block'}
                overflow-y-auto
                ${!isChatInputCentered && isChatInputOpen 
                    ? 'bottom-[calc(1vh+var(--input-height))]' 
                    : 'bottom-0'}`}
                style={{ 
                    '--input-height': inputHeight
                } as React.CSSProperties}
            >
                <HistoryChat historyChat={chatHistory}/>
            </div>

            {/* Chat Input */}
            <div ref={inputRef}
                className={`absolute 
                left-1/2 transform -translate-x-1/2 bg-blue flex flex-col justify-center 
                transition-all duration-500 ease-in-out
                ${isChatInputCentered ? 'w-[40vw]' : 'w-[80%]'}
                ${isChatInputCentered ? 'top-1/2 -translate-y-1/2' : 'bottom-[1vh]'} 
                ${isChatInputOpen ? 'visible' : 'hidden'}`}
            >
                {/*Title container*/}
                <div className={`flex items-center justify-center gap-2 mx-4 mb-8 ${isChatInputCentered ? 'visible' : 'hidden'}`}>
                    <img 
                        src="/logo/logo.jpg" 
                        alt="Logo" 
                        className="w-16 h-16 object-cover rounded-full"
                    />
                    <h1 className="text-4xl ml-4 font-bold">Lovelytics</h1>
                </div>
                
                <div className="border mb-4 bg-gray-200 rounded-[1.5rem]">
                    <InputChat/>
                    <ButtonsChat isProfessionOpen={isProfessionOpen} setIsProfessionOpen={setIsProfessionOpen} />
                </div>

                {/* Suggestions */}
                <div className={`mx-2 ${isProfessionOpen ? 'visible' : 'hidden'}`}>
                    <SuggestionsChat/>
                </div>
            </div>

            {/* Chat input toggle button */}
            <div className={`absolute bottom-[5vh] left-[5vh] w-16 h-16 rounded-full 
                bg-blue-500 hover:bg-blue-600 cursor-pointer 
                flex items-center justify-center 
                transform transition-all duration-200 hover:scale-105 
                shadow-lg hover:shadow-xl 
                ${isChatInputCentered ? 'opacity-0' : 'opacity-100'}`}
                onClick={() => {
                    setIsChatInputOpen(!isChatInputOpen);
                }}
            >
                {isChatInputOpen ? (
                    <svg xmlns="http://www.w3.org/2000/svg" 
                        className="h-10 w-10 text-white" 
                        fill="none" 
                        viewBox="0 0 24 24" 
                        stroke="currentColor"
                    >
                        <path strokeLinecap="round" 
                            strokeLinejoin="round" 
                            strokeWidth={2} 
                            d="M6 18L18 6M6 6l12 12" 
                        />
                    </svg>
                ) : (
                    <svg xmlns="http://www.w3.org/2000/svg" 
                        className="h-10 w-10 text-white" 
                        fill="none" 
                        viewBox="0 0 24 24" 
                        stroke="currentColor"
                    >
                        <path strokeLinecap="round" 
                            strokeLinejoin="round" 
                            strokeWidth={2} 
                            d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" 
                        />
                    </svg>
                )}
            </div>
        </div>
    );
};

const Chat: React.FC = () => {
    return (
        <ChatHistoryProvider>
            <ChatProvider>
                <SuggestionsProvider>
                    <ChatContent />
                </SuggestionsProvider>
            </ChatProvider>
        </ChatHistoryProvider>
    );
};

export default Chat;