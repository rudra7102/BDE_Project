import { useState, useRef } from "react";
import axios from "axios";

interface Faculty {
  name: string;
  specialization: string;
  bio: string;
  profile_url: string;
}

const API_URL =
  window.location.hostname === "localhost" ||
  window.location.hostname === "127.0.0.1"
    ? "http://127.0.0.1:8000"
    : "https://bde-project-c4fi.onrender.com";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Faculty[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const resultsRef = useRef<HTMLDivElement>(null);

  const searchFaculty = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError("");
    setResults([]);

    try {
      const response = await axios.post(
        `${API_URL}/recommend`,
        { query, top_k: 5 },
        { timeout: 60000 }
      );

      setResults(response.data);

      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: "smooth" });
      }, 100);

    } catch (err) {
      setError("Backend temporarily unavailable.");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen w-screen bg-gray-50">

      {/* NAVBAR */}
      <nav className="w-full flex justify-between items-center px-12 py-5 bg-white shadow-md">
        <h1 className="text-2xl font-bold text-emerald-600 tracking-wide">
          Faculty Finder
        </h1>
      </nav>

      {/* HERO SECTION */}
      <section className="w-full bg-gradient-to-r from-emerald-700 to-teal-600 text-white py-32 text-center">
        <div className="max-w-5xl mx-auto px-4">
          <h2 className="text-5xl font-bold mb-6 leading-tight">
            Find the Right Faculty for Your Research — Using AI
          </h2>

          <p className="text-lg mb-12 opacity-90">
            Discover faculty expertise beyond titles using intelligent semantic search.
          </p>

          <div className="flex justify-center">
            <div className="bg-white flex rounded-2xl shadow-2xl w-full max-w-2xl overflow-hidden">
              <input
                type="text"
                placeholder="e.g. Cybersecurity, Machine Learning..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && searchFaculty()}
                className="flex-1 px-6 py-4 text-black outline-none text-lg"
              />

              <button
                onClick={searchFaculty}
                className="bg-emerald-600 text-white px-10 text-lg font-semibold hover:bg-emerald-700 transition duration-300"
              >
                {loading ? "Searching..." : "Search"}
              </button>
            </div>
          </div>

          {error && (
            <p className="text-red-200 mt-6 font-medium">
              {error}
            </p>
          )}
        </div>
      </section>

      {/* RESULTS SECTION */}
      <div ref={resultsRef} className="max-w-6xl mx-auto mt-20 px-6 pb-24">

        {results.length > 0 && (
          <h3 className="text-4xl font-bold mb-14 text-center text-gray-800">
            Recommended Faculty
          </h3>
        )}

        {loading && (
          <div className="text-center text-gray-600 text-lg">
            Finding best matches...
          </div>
        )}

        <div className="grid md:grid-cols-2 gap-12">
          {results.map((faculty, index) => (
            <div
              key={index}
              className="bg-white p-8 rounded-3xl shadow-xl hover:shadow-2xl transition duration-300 border border-gray-100 hover:-translate-y-2 transform"
            >
              <h4 className="text-2xl font-bold text-emerald-700 mb-2">
                {faculty.name}
              </h4>

              <p className="text-sm uppercase tracking-wide text-emerald-500 font-semibold">
                {faculty.specialization}
              </p>

              <p className="text-gray-600 mt-4 leading-relaxed">
                {faculty.bio}
              </p>

              <button
                onClick={() => window.open(faculty.profile_url, "_blank")}
                className="mt-6 px-6 py-2 bg-emerald-600 text-white rounded-xl hover:bg-emerald-700 transition duration-300"
              >
                View Profile
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
