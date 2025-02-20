import React, { useState, useEffect } from 'react';
import { SubTask } from '@/types/ChatMessageType';
import { useChat } from '@/contexts/chat/ChatContext';
import { sendSubTasksToLLM } from '@/services/api';

const SubTaskWindow: React.FC = () => {
    const { subTasks, setSubTasks } = useChat();
    const [editingIndex, setEditingIndex] = useState<number | null>(null);
    const [editingTask, setEditingTask] = useState<SubTask | null>(null);
    const { setIsSubTaskWindowOpen } = useChat();

    const handleEdit = (index: number, task: SubTask) => {
        setEditingIndex(index);
        setEditingTask({ ...task });
    };

    const handleSave = (index: number) => {
        if (editingTask) {
            handleSubTaskUpdate(index, editingTask);
            setEditingIndex(null);
            setEditingTask(null);
        }
    };

    
    const handleSubTaskUpdate = (index: number, updatedTask: SubTask) => {
        const newSubTasks = [...subTasks];
        newSubTasks[index] = updatedTask;
        setSubTasks(newSubTasks);
    };

    useEffect(() => {
        
        console.log("SubTasks in window:", subTasks);
    }, [subTasks]);

    return (
        <div className="w-full h-full bg-white p-6 overflow-y-auto">
            <h2 className="text-2xl font-bold mb-6">Project Sub Tasks</h2>
            {subTasks.length === 0 ? (
                <p className="text-center text-gray-500">No subtasks available</p>
            ) : (
                <div className="flex flex-col items-center gap-4">
                    {subTasks.map((task, index) => (
                        <div key={index} className="w-[80%] bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                            {editingIndex === index ? (
                                // Edit mode
                                <div className="flex flex-col gap-4">
                                    <input
                                        type="text"
                                        value={editingTask?.title || ''}
                                        onChange={(e) => setEditingTask(prev => prev ? { ...prev, title: e.target.value } : null)}
                                        className="text-xl font-semibold p-2 border rounded"
                                    />
                                    <textarea
                                        value={editingTask?.description || ''}
                                        onChange={(e) => setEditingTask(prev => prev ? { ...prev, description: e.target.value } : null)}
                                        className="w-full p-2 border rounded min-h-[100px]"
                                    />
                                    <div className="flex justify-end gap-2">
                                        <button
                                            onClick={() => setEditingIndex(null)}
                                            className="px-4 py-2 text-gray-600 hover:text-gray-800"
                                        >
                                            Cancel
                                        </button>
                                        <button
                                            onClick={() => handleSave(index)}
                                            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                                        >
                                            Save
                                        </button>
                                    </div>
                                </div>
                            ) : (
                                // View mode
                                <div>
                                    <div className="flex justify-between items-start mb-4">
                                        <h3 className="text-xl font-semibold">{task.title}</h3>
                                        <button
                                            onClick={() => handleEdit(index, task)}
                                            className="text-blue-500 hover:text-blue-600"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                                            </svg>
                                        </button>
                                    </div>
                                    <p className="text-gray-600 whitespace-pre-wrap">{task.description}</p>
                                </div>
                            )}
                        </div>
                    ))}
                    <button 
                        onClick={() => {
                            sendSubTasksToLLM(subTasks);
                            setIsSubTaskWindowOpen(false);
                        }}
                        className="mt-4 px-6 py-3 bg-blue-500 text-white rounded-lg 
                            hover:bg-blue-600 transition-colors duration-200
                            flex items-center gap-2 shadow-md hover:shadow-lg"
                    >
                        <span>Process Tasks with AI</span>
                        <svg 
                            xmlns="http://www.w3.org/2000/svg" 
                            className="h-5 w-5" 
                            viewBox="0 0 20 20" 
                            fill="currentColor"
                        >
                            <path fillRule="evenodd" 
                                d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" 
                                clipRule="evenodd" 
                            />
                        </svg>
                    </button>
                </div>
            )}
        </div>
    );
};

export default SubTaskWindow; 