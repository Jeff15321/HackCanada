import { Model } from '@/types/ModelType';
import { calculateRarity } from '@/components/layout/FlowerViews/ImageAnalysis';

export const searchModels = (models: Model[], searchTerm: string): Model[] => {
  const lowerSearchTerm = searchTerm.toLowerCase().trim();
  
  return models.filter(model => {
    // Search by name
    const nameMatch = model.name.toLowerCase().includes(lowerSearchTerm);
    
    // Search by rarity
    const stats = {
      colorVibrancy: model.parameters?.colorVibrancy || { score: 0, explanation: '' },
      leafAreaIndex: model.parameters?.leafAreaIndex || { score: 0, explanation: '' },
      wilting: model.parameters?.wilting || { score: 0, explanation: '' },
      spotting: model.parameters?.spotting || { score: 0, explanation: '' },
      symmetry: model.parameters?.symmetry || { score: 0, explanation: '' }
    };
    const rarity = calculateRarity(stats).toLowerCase();
    const rarityMatch = rarity.includes(lowerSearchTerm);

    return nameMatch || rarityMatch;
  });
}; 