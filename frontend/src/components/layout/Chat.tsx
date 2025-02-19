import React, { useState } from 'react';
import InputChat from "@/components/chat/InputChat"
import ButtonsChat from "@/components/chat/ButtonsChat"
import SuggestionsChat from "@/components/chat/SuggestionsChat"
import { ChatProvider, useChat } from '@/contexts/chat/ChatContext';
import { SuggestionsProvider } from '@/contexts/chat/SuggestionsContext';
import HistoryChat from '../chat/HistoryChat';
import { HistoryChatType } from '@/types/ChatMessageType'

const ChatContent: React.FC = () => {
    const { isInputCentered } = useChat();
    const [isProfessionOpen, setIsProfessionOpen] = useState(false);
    const [isChatInputOpen, setIsChatInputOpen] = useState(true);

    const historyChat: HistoryChatType[] = [
        {
            message: '# Hello\n\nThis is a longer markdown message that provides more detail. It can include various elements such as **bold text**, *italic text*, and even lists:\n\n- Item 1\n- Item 2\n- Item 3\n\nAdditionally, you can add links like [this](https://example.com) or images:\n\n![Alt text](https://via.placeholder.com/150)\n\nFeel free to expand upon this message as needed.',
            is_user: false,
            file_name: 'test.txt',
            date: new Date(),
            user_id: 1
        },
        {
            message: 'Hello',
            is_user: true,
            file_name: 'test.txt',
            date: new Date(),
            user_id: 1
        },
        {
            message: 'Hello',
            is_user: false,
            file_name: 'test.txt',
            date: new Date(),
            user_id: 1
        }
    ]
    return (
        <div className="relative w-full h-full bg-gray-100">
            <div className='absolute top-0 left-[10%] w-[80%] h-full'>
                <HistoryChat historyChat={historyChat}/>
            </div>
            <div className={`absolute 
                            left-1/2 transform -translate-x-1/2 bg-blue flex flex-col justify-center 
                            transition-all duration-500 ease-in-out
                            ${isInputCentered ? 'w-[40vw]' : 'w-[80%] opacity-50 hover:opacity-100'}
                            ${isInputCentered ? 'top-1/2 -translate-y-1/2' : 'bottom-[1vh]'} 
                            ${isChatInputOpen ? 'visible' : 'hidden'}`}>
                {/*Title container*/}
                <div className={`flex items-center justify-center gap-2 mx-4 mb-8 ${isInputCentered ? 'opacity-100' : 'opacity-0'}`}>
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
            <div className='absolute bottom-[5vh] left-[5vh] w-16 h-16 rounded-full 
                bg-blue-500 hover:bg-blue-600 cursor-pointer 
                flex items-center justify-center 
                transform transition-all duration-200 hover:scale-105 
                shadow-lg hover:shadow-xl'
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
        <ChatProvider>
            <SuggestionsProvider>
                <ChatContent />
            </SuggestionsProvider>
        </ChatProvider>
    );
};

export default Chat;