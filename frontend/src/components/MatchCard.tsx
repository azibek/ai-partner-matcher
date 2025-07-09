import type { PartnerMatch } from '../api/match';
import { useState } from 'react';
import copy from 'copy-to-clipboard';

const MatchCard = ({ match }: { match: PartnerMatch }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    copy(match.ai_drafted_email);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <div className="bg-white p-5 shadow-md rounded-xl border border-gray-200 relative">
      <div className="flex justify-between items-start mb-2">
        <h3 className="text-xl font-bold">{match.company_name}</h3>
        <span className="text-sm text-gray-600">{match.fit_score.toFixed(1)}% fit</span>
      </div>
      <p className="text-sm text-gray-500 mb-1"><strong>Industry:</strong> {match.industry}</p>
      <p className="text-sm text-gray-500 mb-1"><strong>Contact:</strong> {match.decision_maker} ({match.contact_email})</p>
      <p className="text-sm text-gray-500 mb-3"><strong>Domain:</strong> {match.domain}</p>
      <div className="bg-gray-50 border border-gray-200 p-3 rounded text-sm text-gray-700 whitespace-pre-line">
        {match.ai_drafted_email}
      </div>
      <button
        onClick={handleCopy}
        className="mt-2 text-xs bg-blue-600 text-white py-1 px-3 rounded hover:bg-blue-700"
      >
        {copied ? 'Copied!' : 'Copy Email'}
      </button>
    </div>
  );
};

export default MatchCard;
