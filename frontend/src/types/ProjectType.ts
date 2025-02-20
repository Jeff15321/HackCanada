import { ChatMessageType } from "./ChatMessageType";
import { Collaborator } from "./CollaboratorType";

export interface Project {
    id: string;
    name: string;
    user_id: string;
    created_at: string;
    is_public: boolean;
    collaborators: Collaborator[];
    chat_history: ChatMessageType[];
}