export interface Model {
    glbFileUrl: string;
    parameters: {
        colorVibrancy: {
            score: number;
            explanation: string;
        };
        leafAreaIndex: {
            score: number;
            explanation: string;
        };
        wilting: {
            score: number;
            explanation: string;
        };
        spotting: {
            score: number;
            explanation: string;
        };
        symmetry: {
            score: number;
            explanation: string;
        };
    };
    name: string;
    walletID: string;
    price: number;
    id: string;
    imageUrl?: string;
    special?: { attribute: string; rarity: number; }[];
    description?: string;
}
