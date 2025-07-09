// src/pages/Results.tsx
import { useEffect, useState, useRef } from 'react';
import { fetchMatches } from '../api/match';
import type { PartnerMatch } from '../api/match';
import MatchCard from '../components/MatchCard';

const Results = () => {
  const [matches, setMatches] = useState<PartnerMatch[]>([]);
  const [loading, setLoading] = useState(true);
  const description = localStorage.getItem('product_description') || '';

  const hasFetched = useRef(false);

  useEffect(() => {
    if (hasFetched.current || !description) return;
    hasFetched.current = true;
    fetchMatches(description)
      .then(setMatches)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen p-6 bg-gray-50">
      <h2 className="text-2xl font-semibold mb-4">Suggested Strategic Partners</h2>
      {loading && <p>Loading matches...</p>}
      {!loading && matches.length === 0 && <p>No matches found.</p>}
      <div className="grid gap-4">
        {matches.map((match, i) => (
          <MatchCard key={i} match={match} />
        ))}
      </div>
    </div>
  );
};

export default Results;
