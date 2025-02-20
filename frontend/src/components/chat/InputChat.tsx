import React, { useRef, useEffect, useState } from 'react';
import FileAttachment from './FileAttachment';
import { useChat } from '@/contexts/chat/ChatContext';

const InputChat: React.FC = () => {
    const textareaRef = useRef<HTMLTextAreaElement>(null);
    const [showScroll, setShowScroll] = useState(false);
    const { message, setMessage, selectedFiles, setSelectedFiles, resetInputs, handleChatSubmit, fetchSubTasks } = useChat();

    const handleRemoveFile = (fileToRemove: File) => {
        setSelectedFiles(selectedFiles.filter(file => file !== fileToRemove));
    };

    const adjustHeight = () => {
        const textarea = textareaRef.current;
        if (!textarea) return;

        textarea.style.height = 'auto';
        
        const lineHeight = parseInt(getComputedStyle(textarea).lineHeight) || 20;
        const maxHeight = lineHeight * 8; // 8 rows maximum
        
        setShowScroll(textarea.scrollHeight > maxHeight);
        const newHeight = Math.min(textarea.scrollHeight, maxHeight);
        textarea.style.height = `${newHeight}px`;
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            fetchSubTasks();
            handleChatSubmit();
        }
    };

    // Adjust height when message changes
    useEffect(() => {
        adjustHeight();
    }, [message]);

    // Reset height when resetInputs changes
    useEffect(() => {
        if (resetInputs && textareaRef.current) {
            textareaRef.current.style.height = 'auto';
        }
    }, [resetInputs]);

    return (
        <div>
            <div className="flex ml-4 flex-wrap gap-1 mt-4">
                {selectedFiles.map((file, index) => (
                    <FileAttachment 
                        key={`${file.name}-${index}`}
                        file={file}
                        onRemove={() => handleRemoveFile(file)}
                    />
                ))}
            </div>
            <textarea
                id='ChatInputBar'
                ref={textareaRef}
                value={message}
                onChange={(e) => {
                    setMessage(e.target.value);
                    adjustHeight();
                }}
                onKeyDown={handleKeyDown}
                className={`mx-4 mt-4 w-[calc(100%-2rem)] resize-none
                            bg-transparent text-gray-700
                            text-base placeholder:text-gray-400
                            focus:outline-none
                            ${showScroll ? 'overflow-y-auto' : 'overflow-y-hidden'}`}
                placeholder="Send a message..."
                rows={1}
                style={{ wordWrap: 'break-word' }}
            /> 
        </div>
    );
}

export default InputChat;