export interface TokenData {
  token_id: string;
  owner_id: string;
  metadata: {
    title: string;
    media: string;
    description: string;
    price?: string;
    extra?: string;
  };
  approved_account_ids?: Record<string, number>;
} 