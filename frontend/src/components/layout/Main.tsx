import React, { useState, useEffect } from 'react';
import Sidebar from './Sidebar';
import Home from './Home';
import Login from '../auth/Login';
import Signup from '../auth/Signup';
import { useUser } from '../../contexts/UserContext';
import Chat from './Chat'
import NewProjectModal from '../popup/NewProjectModal';
import { newProject } from '@/services/api';
import { fetchAllProjects } from '@/services/api';

interface Collaborator {
    id: string;
    email: string;
}

interface MainProps {
    CurrentView: 'home' | 'chat';
}

const Main: React.FC<MainProps> = ({ CurrentView }) => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [homeProjects, setHomeProjects] = useState<any[]>([]);

    //user variables
    const { user, setUser } = useUser();

    //authentication variables
    const [isSignup, setIsSignup] = useState(false);

    useEffect(() => {
        if (localStorage.getItem('user')) {
            const user = JSON.parse(localStorage.getItem('user') || '{}');
            setUser(user);
        }
    }, []);

    // Add this function to pass down to Sidebar
    const handleNewChat = () => {
        setIsModalOpen(true);
    };

    if (!user) {
        return isSignup ? (
            <Signup/>
        ) : (
            <Login 
                onSignupClick={() => setIsSignup(true)}
            />
        );
    }

    const handleCreateProject = async (projectName: string, collaborators: Collaborator[], isPublic: boolean) => {
        try {
            if (!user?.id) return;
            const response = await newProject(user.id, projectName, collaborators, isPublic);
            const updatedProjects = await fetchAllProjects(user.id);
          
            setIsModalOpen(false);
            return response;
        } catch (error) {
            console.error('Failed to create project:', error);
            throw error;
        }
    };
    
    return (
        <div className="flex h-screen overflow-hidden">
            <Sidebar 
                isHome={CurrentView === 'home'} 
                onNewChat={handleNewChat}  // Add this prop
            />
            
            <div className="flex-1">
                {CurrentView === 'home' ? (
                    <Home/>
                ) : (
                    <Chat />
                )}
            </div>
            
            {isModalOpen && (
                <NewProjectModal 
                    isOpen={isModalOpen} 
                    onClose={() => setIsModalOpen(false)}
                    onCreateProject={handleCreateProject}
                />
            )}
        </div>
    );
};

export default Main;