export interface Model {
    id: string;
    name: string;
    description: string;
    imageUrl: string;
    image: File;
    attributes: {
        health: number;
        growth: number;
        waterLevel: number;
        sunlight: number;
    }
}
