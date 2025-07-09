// src/pages/Home.tsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!description.trim()) return;

    setLoading(true);
    localStorage.setItem('product_description', description); // Store for results page
    navigate('/results');
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white shadow-xl rounded-2xl p-8 max-w-2xl w-full">
        <h1 className="text-2xl font-bold mb-4 text-center">AI Partner Matcher</h1>
        <form onSubmit={handleSubmit}>
          <label className="block mb-2 font-medium">Describe your product or company:</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={6}
            className="w-full border rounded-lg p-3 text-gray-800 resize-none"
            placeholder="e.g. We build AI-powered analytics tools for retail brands to forecast demand..."
          />
          <button
            type="submit"
            disabled={loading}
            className="mt-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold px-5 py-2 rounded-xl w-full"
          >
            {loading ? 'Loading...' : 'Find Partners'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Home;