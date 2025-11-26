import { QueryResult } from '@/lib/types';
import MovieCard from './MovieCard';

interface SystemColumnProps {
  result: QueryResult | null;
  isLoading: boolean;
  error?: string;
}

export default function SystemColumn({ result, isLoading, error }: SystemColumnProps) {
  const systemName = result?.system_name || 'System';
  const displayName = systemName
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');

  return (
    <div className="flex flex-col h-full">
      <h2 className="text-xl font-bold text-text mb-4 pb-2 border-b border-gray-700">
        {displayName}
      </h2>

      {isLoading && (
        <div className="flex items-center justify-center p-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-accent"></div>
        </div>
      )}

      {error && (
        <div className="bg-error/20 border border-error text-error px-4 py-3 rounded">
          {error}
        </div>
      )}

      {result && !isLoading && (
        <div className="space-y-4">
          {result.reasoning && (
            <div className="bg-gray-800 p-3 rounded text-sm text-gray-300">
              <p className="font-semibold mb-1">Reasoning:</p>
              <p className="italic">{result.reasoning}</p>
            </div>
          )}

          <div className="space-y-3">
            {result.results.length > 0 ? (
              result.results.map((movie) => (
                <MovieCard key={movie.id} movie={movie} />
              ))
            ) : (
              <p className="text-gray-400 text-center p-8">
                No results found
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
