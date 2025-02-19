import { useChat } from "@/contexts/chat/ChatContext";
import { Project } from "../types/ProjectType";
import { ChatMessageType } from "@/types/ChatMessageType"
import { useUser } from "@/contexts/UserContext";
import { useSuggestions } from "@/contexts/chat/SuggestionsContext";

const API_BASE_URL = 'http://localhost:8000/api';

export const newProject = async (
    user_id: string, 
    project_name: string, 
    collaborators: any[],
    isPublic: boolean
) => {
    const response = await fetch(`${API_BASE_URL}/projects/new/`, {
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
        const response = await fetch(`http://localhost:8000/api/v1/projects/?user_id=${userId}`.replace(/\/$/, ''));
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
        const response = await fetch(`${API_BASE_URL}/projects/delete/?project_id=${project_id}`, { method: 'DELETE' });
        if (!response.ok) {
            throw new Error('Failed to delete project');
        }
        return response.status;
    } catch (error) {
        console.error('Error deleting project:', error);
        return [];
    }
};

// export const openWhiteBoard = async (user_id: string, project_id: string) => {
//     try {
//         const response = await fetch(`${API_BASE_URL}/whiteboard/${project_id}/`, {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ user_id, project_id }),
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


// export const uploadWhiteBoard = async (user_id: string, project: Project) => {
//     try {
//         const response = await fetch(`${API_BASE_URL}/upload-whiteboard/`, {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ user_id, project }),
//         });

//         if (!response.ok) {
//             throw new Error('Failed to save project');
//         }

//         const data = await response.json();
//         return data;
//     } catch (error) {
//         console.error('Error saving whiteboard:', error);
//         return null;
//     }
// };


export const PostChatMessage = async (chatMessage: ChatMessageType) => {
    // const response = await fetch(`${API_BASE_URL}/add-rout-here`, {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify(chatMessage),
    // });

    // if (!response.ok) {
    //     throw new Error('Failed to create new project');
    // }
    
    // return response.json();
    console.log('Posting chat message:', chatMessage);
};

export const GetSuggestions = async (profession: string) => {
    const tmp = [
        "Suggestion 1",
        "Suggestion 2222",
        "Sugge 3",
        "Suggestion 42",
        "Suggestion 5",
        "Suggestion 6",
        "Suggestion 7",
        "Suggestion 8",
        "Suggestion 9",
        "Suggestion 10"
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