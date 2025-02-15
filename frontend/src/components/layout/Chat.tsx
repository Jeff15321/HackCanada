import React from 'react';
import InputChat from "@/components/chat/InputChat"
import ButtonsChat from "@/components/chat/ButtonsChat"
import SuggestionsChat from "@/components/chat/SuggestionsChat"
import { ChatProvider } from '@/contexts/ChatContext';

const Chat: React.FC = () => {
    return (
        <ChatProvider>
            <div className="relative w-full h-full bg-gray-100">
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 
                                -translate-y-1/2 bg-blue flex flex-col justify-center 
                                w-[40vw]">
                    {/*Title container*/}
                    <div className="flex items-center justify-center gap-2 mx-4 mb-8">
                        <img 
                            src="/logo/logo.jpg" 
                            alt="Logo" 
                            className="w-16 h-16 object-cover rounded-full"
                        />
                        <h1 className="text-4xl ml-4 font-bold">Lovelytics</h1>
                    </div>
                    
                    <div className="border bg-gray-200 rounded-[1.5rem]">
                        <InputChat />
                        <ButtonsChat />
                    </div>

                    {/* Suggestions */}
                    <div className="mx-2 mt-4">
                        <SuggestionsChat/>
                    </div>
                </div>
            </div>
        </ChatProvider>
    );
};

export default Chat;