'use client';

import { useState } from 'react';
import SearchBar from '@/components/SearchBar';
import SystemColumn from '@/components/SystemColumn';
import { api } from '@/lib/api';
import { QueryResult, SystemName } from '@/lib/types';

export default function Home() {
  const [results, setResults] = useState<Record<string, QueryResult>>({});
  const [loading, setLoading] = useState<Record<string, boolean>>({});
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [currentQuery, setCurrentQuery] = useState<string>('');

  const handleSearch = async (
    query: string,
    systems: SystemName[],
    limit: number
  ) => {
    setCurrentQuery(query);
    setResults({});
    setErrors({});

    // Set loading state for all selected systems
    const loadingState: Record<string, boolean> = {};
    systems.forEach((system) => {
      loadingState[system] = true;
    });
    setLoading(loadingState);

    // Query all systems in parallel
    const promises = systems.map(async (system) => {
      try {
        const result = await api.query(system, query, limit);
        setResults((prev) => ({ ...prev, [system]: result }));
        setLoading((prev) => ({ ...prev, [system]: false }));
      } catch (error) {
        const message =
          error instanceof Error ? error.message : 'Unknown error occurred';
        setErrors((prev) => ({ ...prev, [system]: message }));
        setLoading((prev) => ({ ...prev, [system]: false }));
      }
    });

    await Promise.all(promises);
  };

  const selectedSystems = Object.keys(loading);
  const hasResults = Object.keys(results).length > 0 || Object.keys(errors).length > 0;

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-text mb-2">
            Entertainment Graph
          </h1>
          <p className="text-gray-400">
            Compare retrieval systems side-by-side
          </p>
        </header>

        <div className="mb-8">
          <SearchBar onSearch={handleSearch} isLoading={Object.values(loading).some(l => l)} />
        </div>

        {currentQuery && hasResults && (
          <div className="mb-4">
            <p className="text-gray-400 text-sm">
              Showing results for:{' '}
              <span className="text-text font-medium">&quot;{currentQuery}&quot;</span>
            </p>
          </div>
        )}

        {hasResults && (
          <div className={`grid gap-6 ${
            selectedSystems.length === 1
              ? 'grid-cols-1 max-w-2xl mx-auto'
              : selectedSystems.length === 2
              ? 'grid-cols-1 md:grid-cols-2'
              : 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3'
          }`}>
            {selectedSystems.map((system) => (
              <div key={system} className="bg-card p-6 rounded-lg">
                <SystemColumn
                  result={results[system] || null}
                  isLoading={loading[system] || false}
                  error={errors[system]}
                />
              </div>
            ))}
          </div>
        )}

        {!hasResults && !Object.values(loading).some(l => l) && (
          <div className="text-center py-16">
            <p className="text-gray-400 text-lg">
              Enter a query above to compare retrieval systems
            </p>
          </div>
        )}
      </div>
    </main>
  );
}
