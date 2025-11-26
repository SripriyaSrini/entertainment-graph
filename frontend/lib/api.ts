import { QueryResult, HealthStatus, SystemName } from './types';

export class EntertainmentGraphAPI {
  private baseURL: string;

  constructor(baseURL?: string) {
    this.baseURL = baseURL || process.env.NEXT_PUBLIC_API_URL || 'https://web-production-b84b0.up.railway.app';
  }

  async query(system: SystemName, query: string, limit: number = 5): Promise<QueryResult> {
    const response = await fetch(`${this.baseURL}/query/${system}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, limit }),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async health(): Promise<HealthStatus> {
    const response = await fetch(`${this.baseURL}/health`);

    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status}`);
    }

    return response.json();
  }
}

// Singleton instance
export const api = new EntertainmentGraphAPI();
