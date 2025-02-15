import React from 'react';
import { FaFile, FaImage } from 'react-icons/fa';

interface FileAttachmentProps {
    file: File;
    onRemove: () => void;
}

const FileAttachment: React.FC<FileAttachmentProps> = ({ file, onRemove }) => {
    const fileType = file.type.split('/')[1]?.toUpperCase() || 'FILE';
    const isImage = file.type.startsWith('image/');

    return (
        <div className="flex items-center">
            <div className="flex items-center bg-gray-100 rounded-lg px-3 py-2 group hover:bg-gray-200 transition-colors">
                <div className="relative w-8 h-8 flex items-center justify-center text-gray-500">
                    {isImage ? (
                        <FaImage className="w-6 h-6" />
                    ) : (
                        <FaFile className="w-6 h-6" />
                    )}
            
                </div>
                <span className="ml-2 text-sm text-gray-600 truncate max-w-[200px]">
                    {file.name}
                </span>
                <button 
                    onClick={onRemove}
                    className="ml-2 text-gray-400 hover:text-gray-600 opacity-0 group-hover:opacity-100 transition-opacity"
                >
                    ×
                </button>
            </div>
        </div>
    );
};

export default FileAttachment; 