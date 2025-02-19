import React, { useEffect, useState } from 'react';
import { Menu, X, Settings, Code, Database, FileText, Home, User, MessageSquarePlus } from 'lucide-react';
import { useProject } from '../../contexts/ProjectContext';
import { useUser } from '../../contexts/UserContext';
import { useRouter } from 'next/router';
import { fetchAllProjects } from '@/services/api';

interface SidebarProps {
    isHome: boolean;
    onNewChat: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isHome, onNewChat }) => {
    const { project, setProject } = useProject();
    const { user, setUser } = useUser();
    const router = useRouter();
    const [homeProjects, setHomeProjects] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    
    // Move state declarations inside the component
    const [isMenuMode, setIsMenuMode] = useState(true);
    const [currentSection, setCurrentSection] = useState<'home' | 'settings' | 'docs' | 'account'>('home');
    const [apiMessage, setApiMessage] = useState<string | null>(null);

    useEffect(() => {
        const loadProjects = async () => {
            if (isLoading || !user?.id) return;
            
            setIsLoading(true);
            try {
                const fetchedProjects = await fetchAllProjects(user.id);
                if (fetchedProjects) {
                    console.log('Fetched projects:', fetchedProjects);
                    setHomeProjects(fetchedProjects);
                }
            } catch (error) {
                console.error('Error loading projects:', error);
            } finally {
                setIsLoading(false);
            }
        };

        loadProjects();
    }, [user?.id, isLoading]);

    const handleProjectClick = (projectId: string) => {
        router.push(`/chat/${projectId}`);
    };

    const testApi = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/test');
            const data = await response.json();
            setApiMessage(data.message);
            setTimeout(() => setApiMessage(null), 3000);
        } catch (error) {
            setApiMessage('Failed to connect to API');
            setTimeout(() => setApiMessage(null), 3000);
        }
    };

    const renderContent = () => {
        switch (currentSection) {
            case 'home':
                return (
                    <div className="space-y-4">
                        <h3 className="font-medium">Welcome Back!</h3>
                    </div>
                );
            case 'account':
                return (
                    <div className="space-y-4">
                        <div className="text-center">
                            <div className="w-20 h-20 bg-gray-200 rounded-full mx-auto mb-3 flex items-center justify-center">
                                <User size={40} className="text-gray-500" />
                            </div>
                            <h3 className="font-medium">{user?.email || 'Not logged in'}</h3>
                        </div>
                        <div className="space-y-2 pt-4">
                            <button className="w-full p-2 text-left hover:bg-gray-100 rounded">
                                Profile Settings
                            </button>
                            <button className="w-full p-2 text-left hover:bg-gray-100 rounded">
                                Preferences
                            </button>
                            <button 
                                className="w-full p-2 text-left text-red-600 hover:bg-red-50 rounded"
                                onClick={() => {
                                    setUser(null);
                                    localStorage.removeItem('user');
                                }}
                            >
                                Sign Out
                            </button>
                        </div>
                    </div>
                );
           
            case 'settings':
                return (
                    <div className="space-y-4">
                        <h3 className="font-medium">Settings</h3>
                        <div className="space-y-2">
                            <div className="flex items-center justify-between">
                                <span>Dark Mode</span>
                                <button className="p-2 bg-gray-100 rounded">Toggle</button>
                            </div>
                            <div className="flex items-center justify-between">
                                <span>Grid Size</span>
                                <input type="number" className="w-20 p-1 border rounded" />
                            </div>
                        </div>
                    </div>
                );
            
            case 'docs':
                return (
                    <div className="space-y-4">
                        <button 
                            onClick={onNewChat}
                            className="w-full p-2 bg-blue-500 text-white rounded-lg
                                     flex items-center justify-center gap-2
                                     hover:bg-blue-600 transition-colors duration-200
                                     shadow-sm"
                        >
                            <MessageSquarePlus size={20} />
                            <span className="font-medium">New Chat</span>
                        </button>
                        
                        <div className="flex flex-col gap-2 mt-4">
                            {homeProjects.map((project, index) => (
                                <button key={index}
                                    onClick={() => handleProjectClick(project.id)}
                                    className="w-full p-2.5 bg-white text-gray-700 rounded-lg
                                            border border-gray-200
                                            flex items-center gap-3
                                            hover:bg-gray-50 hover:border-gray-300
                                            transition-all duration-200
                                            text-left group"
                                >
                                    <div className="flex-1 min-w-0">
                                        <span className="font-medium truncate block">{project.name}</span>
                                        <span className="text-xs text-gray-400 block">
                                            {new Date(project.created_at).toLocaleDateString()}
                                        </span>
                                    </div>
                                </button>
                            ))}
                        </div>
                    </div>
                );
        }
    };

    return (
        <div className="relative left-0 top-0 w-[15vw] h-full bg-white shadow-lg flex flex-col">
            <div className="p-4 border-b flex justify-between items-center">
                <span className="font-semibold text-gray-700">
                    {isMenuMode ? 'Menu' : currentSection.charAt(0).toUpperCase() + currentSection.slice(1)}
                </span>
                <button 
                    onClick={() => setIsMenuMode(!isMenuMode)}
                    className="p-1 hover:bg-gray-100 rounded"
                >
                    {isMenuMode ? <X size={20} /> : <Menu size={20} />}
                </button>
            </div>

            <div className="flex-1 overflow-auto">
                {isMenuMode ? (
                    <div className="p-2 space-y-1">
                        <button 
                            onClick={() => { 
                                router.push('/');
                            }}
                            className="w-full p-2 text-left hover:bg-gray-100 rounded flex items-center gap-2"
                        >
                            <Home size={18} /> Home
                        </button>
    
                        <button 
                            onClick={() => { setCurrentSection('settings'); setIsMenuMode(false); }}
                            className="w-full p-2 text-left hover:bg-gray-100 rounded flex items-center gap-2"
                        >
                            <Settings size={18} /> Settings
                        </button>
                        <button 
                            onClick={() => { setCurrentSection('docs'); setIsMenuMode(false); }}
                            className="w-full p-2 text-left hover:bg-gray-100 rounded flex items-center gap-2"
                        >
                            <FileText size={18} /> Docs
                        </button>
                        <button 
                            onClick={() => { setCurrentSection('account'); setIsMenuMode(false); }}
                            className="w-full p-2 text-left hover:bg-gray-100 rounded flex items-center gap-2"
                        >
                            <User size={18} /> Account
                        </button>
                    </div>
                ) : (
                    <div className="p-4">
                        {renderContent()}
                    </div>
                )}
            </div>

            <div className="p-4 border-t mt-auto">
                <button
                    onClick={testApi}
                    className="w-full p-2 text-sm bg-gray-100 hover:bg-gray-200 
                             rounded-lg transition-colors duration-200 
                             flex items-center justify-center gap-2"
                >
                    <Code size={16} />
                    Test API Connection
                </button>
                
                {apiMessage && (
                    <div className="mt-2 text-sm text-center p-2 rounded-lg 
                                  bg-green-100 text-green-700 border border-green-200">
                        {apiMessage}
                    </div>
                )}
            </div>
        </div>
    );
}; 

export default Sidebar;