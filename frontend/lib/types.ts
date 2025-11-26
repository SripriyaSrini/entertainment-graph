export interface Movie {
  id: string;
  title: string;
  year: number;
  director: string[];
  genres: string[];
  plot_summary?: string;
  score?: number;
  explanation?: string;
}

export interface QueryResult {
  results: Movie[];
  reasoning: string;
  system_name: string;
}

export interface HealthStatus {
  status: string;
  pure_vector: boolean;
  graphiti: boolean;
  openmemory: boolean;
}

export type SystemName = 'pure_vector' | 'graphiti' | 'openmemory';
