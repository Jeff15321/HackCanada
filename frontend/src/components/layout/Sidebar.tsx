import React, { useState } from 'react';
import { Menu, X, Settings, Code, Database, FileText, Home, User } from 'lucide-react';
import { useProject } from '../../contexts/ProjectContext';
import { useUser } from '../../contexts/UserContext';
import { useRouter } from 'next/router';

interface SidebarProps {
    isHome: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({ isHome }) => {
    const { project, setProject } = useProject();
    const { user, setUser } = useUser();
    const router = useRouter();
    
    // Move state declarations inside the component
    const [isMenuMode, setIsMenuMode] = useState(true);
    const [currentSection, setCurrentSection] = useState<'home' | 'settings' | 'code' | 'data' | 'docs' | 'account'>('home');

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
            case 'code':
                return (
                    <div className="space-y-4">
                        <h3 className="font-medium">Generated Code</h3>
                        <pre className="bg-gray-100 p-2 rounded text-sm">
                            {`// Your code here\nfunction example() {\n  return true;\n}`}
                        </pre>
                    </div>
                );
            case 'data':
                return (
                    <div className="space-y-4">
                        <h3 className="font-medium">Data Management</h3>
                        <div className="space-y-2">
                            <button className="w-full p-2 bg-green-500 text-white rounded">
                                Import Data
                            </button>
                            <button className="w-full p-2 bg-blue-500 text-white rounded">
                                Export Data
                            </button>
                        </div>
                    </div>
                );
            case 'docs':
                return (
                    <div className="space-y-4">
                        <h3 className="font-medium">Documentation</h3>
                        <div className="space-y-2 text-sm">
                            <p>Learn how to use the node editor...</p>
                            <a href="#" className="text-blue-500 hover:underline">View Full Docs</a>
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
                            onClick={() => { setCurrentSection('code'); setIsMenuMode(false); }}
                            className="w-full p-2 text-left hover:bg-gray-100 rounded flex items-center gap-2"
                        >
                            <Code size={18} /> Code
                        </button>
                        <button 
                            onClick={() => { setCurrentSection('data'); setIsMenuMode(false); }}
                            className="w-full p-2 text-left hover:bg-gray-100 rounded flex items-center gap-2"
                        >
                            <Database size={18} /> Data
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
        </div>
    );
}; 

export default Sidebar;