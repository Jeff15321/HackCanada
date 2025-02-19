import React, { useState } from 'react';
import InputChat from "@/components/chat/InputChat"
import ButtonsChat from "@/components/chat/ButtonsChat"
import SuggestionsChat from "@/components/chat/SuggestionsChat"
import { ChatProvider, useChat } from '@/contexts/chat/ChatContext';
import { SuggestionsProvider } from '@/contexts/chat/SuggestionsContext';

const ChatContent: React.FC = () => {
    const { isInputCentered } = useChat();
    const [isProfessionOpen, setIsProfessionOpen] = useState(false);

    
    return (
        <div className="relative w-full h-full bg-gray-100">
            <div className={`absolute ${isInputCentered ? 'top-1/2 -translate-y-1/2' : 'bottom-[1vh]'} 
                            left-1/2 transform -translate-x-1/2 bg-blue flex flex-col justify-center 
                            w-[40vw] transition-all duration-500 ease-in-out`}>
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
                    <InputChat />
                    <ButtonsChat isProfessionOpen={isProfessionOpen} setIsProfessionOpen={setIsProfessionOpen} />
                </div>

                {/* Suggestions */}
                <div className={`mx-2 ${isProfessionOpen ? 'visible' : 'hidden'}`}>
                    <SuggestionsChat/>
                </div>
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