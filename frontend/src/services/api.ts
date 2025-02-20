import { useChat } from "@/contexts/chat/ChatContext";
import { Project } from "../types/ProjectType";
import { ChatMessageType } from "@/types/ChatMessageType"
import { useUser } from "@/contexts/UserContext";
import { useSuggestions } from "@/contexts/chat/SuggestionsContext";

const API_BASE_URL = 'http://localhost:8000';

export const newProject = async (
    user_id: string, 
    project_name: string, 
    collaborators: any[],
    isPublic: boolean
) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/projects/new/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            user_id, 
            project_name, 
            collaborators,
            is_public: isPublic 
        }),
    });

    if (!response.ok) {
        throw new Error('Failed to create new project');
    }

    return response.json();
};

export const fetchAllUsers = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/users/`);
        const data = await response.json();
        return data.users;
    } catch (error) {
        console.error('Error fetching users:', error);
    }
};

export const fetchAllProjects = async (userId: string) => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/projects/all/?user_id=${userId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch projects');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching projects:', error);
        return null;
    }
};

export const deleteProject = async (project_id: string) => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/projects/delete/?project_id=${project_id}`, { 
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        });
        if (!response.ok) {
            throw new Error('Failed to delete project');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error deleting project:', error);
        throw error;
    }
};

//TODO: attach this to the ONET database
export const GetSuggestions = async (profession: string) => {
    const tmp = [
        "Student",
        "Professor",
        "Researcher",
        "Engineer",
        "Designer",
        "Writer",
        "Scientist",
        "Lawyer",
        "Doctor",
        "Businessman"
    ];
    //     try {
//         const response = await fetch(`${API_BASE_URL}/api-link-here`, {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ profession }),
//         });
//         if (response.status === 404) {
//             return null;
//         }
//         if (!response.ok) {
//             throw new Error('Failed to fetch project');
//         }

//         const data = await response.json();
//         return data.project;
//     } catch (error) {
//         console.error('Error opening whiteboard:', error);
//         return null;
//     }
// };

    return tmp   
}

export const LLMChatProcess = async (message: string) => {
    try {
        console.log('Sending message:', message);
        const response = await fetch(`${API_BASE_URL}/api/v1/chat/process`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content: message
            }),
        });

        const data = await response.json();
        console.log('Raw response:', data);

        if (!response.ok) {
            throw new Error(data.detail || 'Failed to process message');
        }

        return data;
    } catch (error) {
        console.error('Error in chat process:', error);
        throw new Error(error instanceof Error ? error.message : 'Unknown error occurred');
    }
};