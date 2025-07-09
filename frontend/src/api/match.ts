// src/api/match.ts
import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';


export type PartnerMatch = {
  company_name: string;
  domain: string;
  industry: string;
  fit_score: number;
  decision_maker: string;
  contact_email: string;
  ai_drafted_email: string;
}

export const fetchMatches = async (description: string): Promise<PartnerMatch[]> => {
  const res = await axios.post(`${BASE_URL}/match`, {
    product_description: description,
  });
  return res.data;
};
