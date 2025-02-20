import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { deleteProject, getProjectChat, newProject } from '../../services/api';
import NewProjectModal from '../popup/NewProjectModal';
import { useUser } from '../../contexts/UserContext';
import { fetchAllProjects } from '../../services/api';
import { Globe, Lock, Users } from 'lucide-react';
import { Project } from '../../types/ProjectType';
import ProjectContextMenu from '../popup/ProjectContextMenu';
import { Collaborator } from '../../types/CollaboratorType';
import { useProject } from '@/contexts/ProjectContext';
import { useChatHistory } from '@/contexts/chat/ChatHistoryContext';
interface ContextMenu {
    show: boolean;
    x: number;
    y: number;
    projectId: string;
}

const Home: React.FC = () => {
    const { user } = useUser();
    const { project, setProject } = useProject();
    const { chatHistory, setChatHistory } = useChatHistory();
    const router = useRouter();
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [contextMenu, setContextMenu] = useState<ContextMenu>({
        show: false,
        x: 0,
        y: 0,
        projectId: ''
    });
    const [homeProjects, setHomeProjects] = useState<Project[]>([]);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        const loadProjects = async () => {
            // If already loading or no user ID, don't proceed
            if (isLoading || !user?.id) return;
            console.log('user', user);

            setIsLoading(true);
            try {
                const fetchedProjects = await fetchAllProjects(user.id);
                if (fetchedProjects) {
                    console.log('Fetched projects:', fetchedProjects); // Debug log
                    setHomeProjects(fetchedProjects);
                }
            } catch (error) {
                console.error('Error loading projects:', error);
            } finally {
                setIsLoading(false);
            }
        };

        loadProjects();
    }, [user?.id]);

    const handleProjectClick = async (projectId: string) => {
        try {
            const projectData = await getProjectChat(projectId);
            setProject(projectData);
            setChatHistory(projectData.chat_history);
            console.log(projectData.chat_history);
            router.push(`/chat/${projectId}`);
        } catch (error) {
            console.error("Error fetching project:", error);
        }
    };

    //right click project panel to open context menu
    const handleContextMenu = (e: React.MouseEvent, projectId: string) => {
        e.preventDefault();
        setContextMenu({
            show: true,
            x: e.pageX,
            y: e.pageY,
            projectId
        });
    };

    const handleEditProject = () => {
        setContextMenu({ ...contextMenu, show: false });
    };

    const handleDeleteProject = async () => {
        try {
            await deleteProject(contextMenu.projectId);
            setHomeProjects(prevProjects => prevProjects.filter(project => project.id !== contextMenu.projectId));
            setContextMenu({ ...contextMenu, show: false });
        } catch (error) {
            console.error('Failed to delete project:', error);
        }
    };

    const handleCreateProject = async (projectName: string, collaborators: Collaborator[], isPublic: boolean) => {
        try {
            if (!user?.id) return;
            const response = await newProject(user.id, projectName, collaborators, isPublic);
            const updatedProjects = await fetchAllProjects(user.id);
            if (updatedProjects) {
                setHomeProjects(updatedProjects);
            }
            setIsModalOpen(false);
            return response;
        } catch (error) {
            console.error('Failed to create project:', error);
            throw error;
        }
    };

    return (
        <div className="w-full h-full bg-gray-50 p-8 overflow-y-auto max-h-screen relative">
            <div className="max-w-4xl mx-auto space-y-8">
                {/* Welcome Section */}
                <div className="bg-white rounded-xl shadow-sm p-6">
                    <h1 className="text-2xl font-bold text-gray-800 mb-2">Welcome to Node Editor</h1>
                    <p className="text-gray-600">Create and manage your node-based workflows</p>
                </div>

                {/* Recent Projects and Quick Actions */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-white rounded-xl shadow-sm p-6 hover:shadow-lg transition-all duration-200">
                        <div className="flex flex-col items-center text-center">
                            <h3 className="text-lg font-medium text-gray-500 mb-3">Total Projects</h3>
                            <p className="text-6xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent leading-none mb-3">
                                {homeProjects.length}
                            </p>
                            <div className="h-1 w-24 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full"></div>
                        </div>
                    </div>

                    <div className="bg-white rounded-xl shadow-sm p-6">
                        <h2 className="text-lg font-semibold text-gray-800 mb-4">Quick Actions</h2>
                        <div className="space-y-3">
                            <button 
                                onClick={() => setIsModalOpen(true)}
                                className="w-full p-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                            >
                                New Project
                            </button>
                            <button className="w-full p-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200">
                                Import Project
                            </button>
                        </div>
                    </div>
                </div>

                {/* Project Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {[...homeProjects].reverse().map(project => (
                        <div 
                            key={project.id}
                            onClick={() => handleProjectClick(project.id)}
                            onContextMenu={(e) => handleContextMenu(e, project.id)}
                            className="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow cursor-pointer"
                        >
                            <div className="flex justify-between items-start mb-4">
                                <h3 className="text-lg font-semibold text-gray-800 truncate">
                                    {project.name}
                                </h3>
                                {project.is_public ? (
                                    <Globe className="text-green-500" size={20} />
                                ) : (
                                    <Lock className="text-gray-500" size={20} />
                                )}
                            </div>
                            
                            <div className="flex items-center text-gray-600 mb-2">
                                <Users size={16} className="mr-2" />
                                <span className="text-sm">
                                    {project.collaborators.length === 0 
                                        ? 'No collaborators' 
                                        : `${project.collaborators.length} collaborator${project.collaborators.length !== 1 ? 's' : ''}`}
                                </span>
                            </div>

                            <div className="flex flex-wrap gap-2 mt-3">
                                {project.collaborators.map(collaborator => (
                                    <span 
                                        key={collaborator.id}
                                        className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full truncate max-w-[150px]"
                                        title={collaborator.email}
                                    >
                                        {collaborator.email}
                                    </span>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>

                {homeProjects.length === 0 && (
                    <div className="text-center py-6">
                        <p className="text-gray-500">No projects yet. Create your first project!</p>
                    </div>
                )}

                {contextMenu.show && (
                    <ProjectContextMenu
                        x={contextMenu.x}
                        y={contextMenu.y}
                        onEdit={handleEditProject}
                        onDelete={handleDeleteProject}
                        onClose={() => setContextMenu({ ...contextMenu, show: false })}
                    />
                )}
            </div>

            {/* Move modal outside the max-w-4xl container but keep it inside the relative parent */}
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

export default Home; 