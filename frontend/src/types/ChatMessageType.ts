export interface ChatMessageType{
    files: File[];
    message: string;
    date: Date;
    user_id: number;
    suggestions: string[];
}

export interface HistoryChatType {
    message: string;
    is_user: boolean;
    file_name: string;
    date: Date;
    user_id: number;
}