import { Movie } from '@/lib/types';

interface MovieCardProps {
  movie: Movie;
}

export default function MovieCard({ movie }: MovieCardProps) {
  return (
    <div className="bg-card p-4 rounded-lg border border-gray-700 hover:border-accent transition-colors">
      <div className="flex justify-between items-start mb-2">
        <div>
          <h3 className="text-lg font-semibold text-text">{movie.title}</h3>
          <p className="text-sm text-gray-400">{movie.year}</p>
        </div>
        {movie.score !== undefined && (
          <span className="text-accent font-medium">
            {movie.score.toFixed(2)}
          </span>
        )}
      </div>

      {movie.director && movie.director.length > 0 && (
        <p className="text-sm text-gray-400 mb-2">
          Dir: {movie.director.join(', ')}
        </p>
      )}

      {movie.genres && movie.genres.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-2">
          {movie.genres.slice(0, 3).map((genre) => (
            <span
              key={genre}
              className="text-xs bg-gray-700 px-2 py-1 rounded"
            >
              {genre}
            </span>
          ))}
        </div>
      )}

      {movie.explanation && (
        <p className="text-sm text-gray-300 mt-2 italic">
          {movie.explanation}
        </p>
      )}
    </div>
  );
}
