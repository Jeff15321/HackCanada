import { Model } from "../types/ModelType";
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const newProject = async (
    user_id: string, 
    project_name: string, 
    collaborators: any[],
    isPublic: boolean
) => {
    const response = await fetch(`${API_BASE_URL}/v1/projects/new/`, {
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
        console.log('Fetching projects for user:', userId);
        const response = await fetch(`${API_BASE_URL}/v1/projects/all/?user_id=${userId}`);
        
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Server error:', errorData);
            throw new Error(`Failed to fetch projects: ${errorData.detail || response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching projects:', error);
        if (error instanceof TypeError && error.message === 'Failed to fetch') {
            console.error('Backend server may be down or unreachable');
        }
        return null;
    }
};

export const deleteProject = async (project_id: string) => {
    try {
        const response = await fetch(`${API_BASE_URL}/v1/projects/delete/?project_id=${project_id}`, { 
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

//TODO: attach the subtask window with Alvin's LLM that she hasn't finished yet
//TODO: make the endpoint in FASTAPI
export const getSubTasks = async (
    user_id: string, 
    project_id: string,
    message: string
) => {
    // const response = await fetch(`${API_BASE_URL}/api/v1/projects/subtasks/`, { 
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify({ 
    //         user_id, 
    //         project_id, 
    //         message
    //     }),
    // });

    // if (!response.ok) {
    //     throw new Error('Failed to create new project');
    // }

    // return response.json();
    return [
        {
            title: "Research Requirements",
            description: "Gather and analyze project requirements through stakeholder interviews, market research, and competitive analysis. Document functional requirements like core features and user interactions, as well as non-functional requirements including performance metrics, security standards, and scalability needs. Create detailed requirement specifications with user stories, acceptance criteria, and technical constraints. Validate requirements with stakeholders and subject matter experts to ensure completeness and accuracy."
        },
        {
            title: "Design Architecture", 
            description: "Create system architecture diagrams and define technical components and their interactions"
        },
        {
            title: "Implementation Plan",
            description: "Break down development tasks and create a detailed implementation timeline"
        },
        {
            title: "Testing Strategy",
            description: "Define testing approach including unit tests, integration tests and acceptance criteria"
        },
        {
            title: "Documentation",
            description: "Prepare technical documentation, API specs and user guides for the project"
        },
        {
            title: "Deployment Planning",
            description: "Plan deployment steps, infrastructure requirements and rollout strategy"
        }
    ]
};

export const newImage = async (
  userId: string,
  imageUrl: string,
  modelName?: string,
  modelDescription?: string,
  modelImageUrl?: string,
  modelImageFile?: File,
  modelAttributes?: Record<string, any>
) => {
  try {
    const formData = new FormData();
    formData.append('userId', userId);
    formData.append('imageUrl', imageUrl);
    if (modelName) formData.append('model_name', modelName);
    if (modelDescription) formData.append('model_description', modelDescription);
    if (modelImageUrl) formData.append('model_image_url', modelImageUrl);
    if (modelImageFile) formData.append('model_image_file', modelImageFile);
    if (modelAttributes) formData.append('model_attributes', JSON.stringify(modelAttributes));

    const response = await axios.post(`${API_BASE_URL}/v1/model/new/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  } catch (error) {
    console.error('Error in newImage:', error);
    throw error;
  }
};