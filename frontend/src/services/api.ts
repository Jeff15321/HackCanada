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
    // Store the image URL temporarily
    if (modelImageFile) {
      const tempImageUrl = URL.createObjectURL(modelImageFile);
      localStorage.setItem(`temp_image_${userId}`, tempImageUrl);
    }

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

    const cleanJsonString = response.data.api2_data.analysis
      .replace(/```json\n/, '')
      .replace(/\n```$/, '')
      .trim();

    const analysisData = JSON.parse(cleanJsonString);

    const getImageUrl = (path: string) => {
      if (path.startsWith('http')) return path;
      return `${API_BASE_URL}${path}`;
    };

    // Use temporary URL if available, otherwise use server URL
    const tempUrl = localStorage.getItem(`temp_image_${userId}`);
    const serverUrl = getImageUrl(response.data.gpt_analysis.glbFileUrl);

    const model: Model = {
      glbFileUrl: serverUrl,
      parameters: analysisData.parameters,
      name: modelName || 'Default Name',
      walletID: userId,
      price: analysisData.price || 0,
      id: userId,
      imageUrl: tempUrl || serverUrl,  // Use temp URL first
      special: analysisData.special || []
    };

    return model;
  } catch (error) {
    console.error('Error in newImage:', error);
    throw error;
  }
};

const getImageUrl = (path: string) => {
  if (path.startsWith('http')) return path;
  return `${API_BASE_URL}${path}`;
};

export const fetchAllModels = async (): Promise<Model[]> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/v1/model/all/`);
    return response.data.map((model: any) => {
      // Check for temporary image URL
      const tempUrl = localStorage.getItem(`temp_image_${model.walletID}`);
      return {
        ...model,
        glbFileUrl: getImageUrl(model.glbFileUrl),
        imageUrl: tempUrl || getImageUrl(model.glbFileUrl)
      };
    });
  } catch (error) {
    console.error('Error fetching models:', error);
    throw error;
  }
};

export const getModelById = async (id: string): Promise<Model> => {
  const allModels = await fetchAllModels();
  const model = allModels.find(m => m.id === id);
  
  if (!model) {
    throw new Error('Model not found');
  }
  
  return model;
};


const BASE_URL = 'https://72ddc6f7069330b4c304c2f4e662bd321785dd91-3000.dstack-prod5.phala.network';


export async function runPipeline() {
    try {
  
      console.log('Calling /api/nft/mint...');
      const mintPayload = {
        token_id: "plant-tee-14",
        receiver_id: "hackcanada.testnet",
        plant_metadata: {
          glb_file_url: "https://example.com/plant.glb",
          parameters: {
            color_vibrancy: { score: 95, explanation: "Vibrant green" },
            leaf_area_index: { score: 85, explanation: "Good coverage" },
            wilting: { score: 90, explanation: "No wilting" },
            spotting: { score: 100, explanation: "No spots" },
            symmetry: { score: 88, explanation: "Good symmetry" }
          },
          name: "TEE Plant #3",
          wallet_id: "hackcanada.testnet",
          price: "1000000000000000000000000"
        }
      };
      const response1 = await fetch(`${BASE_URL}/api/nft/mint`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(mintPayload)
      });
      const result1 = await response1.json();
      console.log('Mint NFT result:', result1);
  
      // 4. Get NFT Metadata
      console.log('Calling /api/nft/metadata/plant-tee-14...');
      const response2 = await fetch(`${BASE_URL}/api/nft/metadata/plant-tee-14`);
      const result2 = await response2.json();
      console.log('NFT Metadata:', result2);
  
      // 5. Get NFT Token Details
      console.log('Calling /api/nft/token/plant-tee-13...');
      const response3 = await fetch(`${BASE_URL}/api/nft/token/plant-tee-14`);
      const result3 = await response3.json();
      console.log('NFT Token Details:', result3);
  
      // 6. Get Tokens for an Owner (Original Owner: hackcanada.testnet) 
      const response4 = await fetch(`${BASE_URL}/api/nft/tokens/hackcanada.testnet`);
      const result4 = await response4.json();
      console.log('Tokens for hackcanada.testnet:', result4);
  
    } catch (error) {
      console.error('Pipeline error:', error);
    }
  }
  
export const runPipelineViaBackend = async (modelData: any): Promise<any> => {
  try {
    // Create a working example payload regardless of input
    const cleanModelData = {
      token_id: "plant-tee-14",
      receiver_id: "hackcanada.testnet",
      plant_metadata: {
        glb_file_url: "https://example.com/plant.glb",
        parameters: {
          color_vibrancy: { score: 95, explanation: "Vibrant green" },
          leaf_area_index: { score: 85, explanation: "Good coverage" },
          wilting: { score: 90, explanation: "No wilting" },
          spotting: { score: 100, explanation: "No spots" },
          symmetry: { score: 88, explanation: "Good symmetry" }
        },
        name: "TEE Plant #3",
        wallet_id: "hackcanada.testnet",
        price: "1000000000000000000000000"
      }
    };

    console.log('Pipeline Payload:', JSON.stringify(cleanModelData, null, 2));
    const response = await axios.post(`${API_BASE_URL}/v1/pipeline/run`, cleanModelData);
    return response.data;
  } catch (error) {
    console.error('Error running pipeline:', error);
    throw error;
  }
};
  
export const mintNFT = async (modelData: any): Promise<any> => {
  try {
    const cleanModelData = {
      token_id: `plant-tee-${modelData.id || '14'}`,
      receiver_id: "hackcanada.testnet", // Always use testnet wallet
      plant_metadata: {
        glb_file_url: modelData.glbFileUrl,
        parameters: {
          color_vibrancy: modelData.parameters.colorVibrancy,  // Changed to snake_case
          leaf_area_index: modelData.parameters.leafAreaIndex, // Changed to snake_case
          wilting: modelData.parameters.wilting,
          spotting: modelData.parameters.spotting,
          symmetry: modelData.parameters.symmetry
        },
        name: modelData.name || "TEE Plant #3",  // Add default name
        wallet_id: "hackcanada.testnet",         // Always use testnet wallet
        price: "1000000000000000000000000"      // Use correct price format
      }
    };

    console.log('Mint Payload:', JSON.stringify(cleanModelData, null, 2));
    const response = await axios.post(`${API_BASE_URL}/v1/nft/mint`, cleanModelData);
    return response.data;
  } catch (error) {
    console.error('Error minting NFT:', error);
    throw error;
  }
};

export const getOwnerTokens = async (walletId: string): Promise<any> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/v1/nft/tokens/${walletId}`);
    return response.data;
  } catch (error) {
    console.error('Error getting owner tokens:', error);
    throw error;
  }
};
  
