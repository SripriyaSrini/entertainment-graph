'use client';

import { useState } from 'react';
import { SystemName } from '@/lib/types';

interface SearchBarProps {
  onSearch: (query: string, systems: SystemName[], limit: number) => void;
  isLoading: boolean;
}

export default function SearchBar({ onSearch, isLoading }: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [selectedSystems, setSelectedSystems] = useState<SystemName[]>([
    'pure_vector',
    'graphiti',
  ]);
  const [limit, setLimit] = useState(5);

  const toggleSystem = (system: SystemName) => {
    setSelectedSystems((prev) =>
      prev.includes(system)
        ? prev.filter((s) => s !== system)
        : [...prev, system]
    );
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && selectedSystems.length > 0) {
      onSearch(query, selectedSystems, limit);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-card p-6 rounded-lg shadow-lg">
      <div className="mb-4">
        <label className="block text-text mb-2 font-medium">
          Search Query
        </label>
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g., Something like Severance but lighter"
          className="w-full bg-background text-text border border-gray-700 rounded px-4 py-3 focus:outline-none focus:border-accent resize-none"
          rows={3}
          disabled={isLoading}
        />
      </div>

      <div className="mb-4">
        <label className="block text-text mb-2 font-medium">
          Systems to Compare
        </label>
        <div className="flex flex-wrap gap-3">
          {(['pure_vector', 'graphiti', 'openmemory'] as SystemName[]).map(
            (system) => (
              <label
                key={system}
                className="flex items-center space-x-2 cursor-pointer"
              >
                <input
                  type="checkbox"
                  checked={selectedSystems.includes(system)}
                  onChange={() => toggleSystem(system)}
                  disabled={isLoading}
                  className="w-4 h-4 text-accent bg-background border-gray-700 rounded focus:ring-accent"
                />
                <span className="text-text capitalize">
                  {system.replace('_', ' ')}
                </span>
              </label>
            )
          )}
        </div>
      </div>

      <div className="mb-4">
        <label className="block text-text mb-2 font-medium">
          Results Limit
        </label>
        <div className="flex gap-3">
          {[3, 5, 10].map((value) => (
            <label
              key={value}
              className="flex items-center space-x-2 cursor-pointer"
            >
              <input
                type="radio"
                name="limit"
                value={value}
                checked={limit === value}
                onChange={() => setLimit(value)}
                disabled={isLoading}
                className="w-4 h-4 text-accent bg-background border-gray-700 focus:ring-accent"
              />
              <span className="text-text">{value}</span>
            </label>
          ))}
        </div>
      </div>

      <button
        type="submit"
        disabled={isLoading || !query.trim() || selectedSystems.length === 0}
        className="w-full bg-accent text-white font-medium py-3 rounded hover:bg-blue-600 disabled:bg-gray-600 disabled:cursor-not-allowed transition-colors"
      >
        {isLoading ? 'Searching...' : 'Search'}
      </button>
    </form>
  );
}
