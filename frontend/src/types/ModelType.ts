export interface Model {
    id: string;
    name: string;
    description: string;
    imageUrl: string;
    image: File;
    threeDModel: File | null;
    attributes: {
        shape: number;
        color: number;
        health: number;
        development: number;
        attributes: {
            attribute: string;
            rarity: number;
        }[];
    }
}
