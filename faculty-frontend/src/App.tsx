import { useState } from "react";
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

const searchFaculty = async () => {
  if (!query.trim()) return;

  console.log("Sending request...");

  setLoading(true);
  setError("");
  setResults([]);

  try {
    const response = await axios.post(
      `${API_URL}/recommend`,
      { query, top_k: 5 },
      { timeout: 15000 }
    );

    console.log("RESPONSE RECEIVED:", response.data);

    setResults(response.data);
  } catch (err: any) {
    console.error("AXIOS ERROR:", err);
    setError("Backend temporarily unavailable.");
  }

  console.log("Request finished");

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

      {/* HERO */}
      <section className="w-full bg-gradient-to-r from-emerald-700 to-teal-600 text-white py-32 text-center">
        <div className="max-w-5xl mx-auto px-4">
          <h2 className="text-5xl font-bold mb-6 leading-tight">
            Find the Right Faculty for Your Research — Using AI
          </h2>

          <p className="text-lg mb-12 opacity-90">
            Discover faculty expertise beyond titles using intelligent semantic search.
          </p>

          <div className="flex justify-center">
            <div className="bg-white flex rounded-xl shadow-2xl w-full max-w-2xl overflow-hidden">
              <input
                type="text"
                placeholder="e.g. Machine Learning"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && searchFaculty()}
                className="flex-1 px-6 py-4 text-black outline-none text-lg"
              />

              <button
                onClick={searchFaculty}
                className="bg-emerald-600 text-white px-10 text-lg font-semibold hover:bg-emerald-700 transition"
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

      {/* RESULTS */}
      <div className="max-w-6xl mx-auto mt-20 px-6 pb-20">
        {results.length > 0 && (
          <h3 className="text-3xl font-semibold mb-12 text-center text-gray-800">
            Recommended Faculty
          </h3>
        )}

        <div className="grid md:grid-cols-2 gap-10">
          {results.map((faculty, index) => (
            <a
              key={index}
              href={faculty.profile_url}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-2xl transition duration-300 block hover:-translate-y-1"
            >
              <h4 className="text-2xl font-bold text-emerald-700 mb-3">
                {faculty.name}
              </h4>

              <p className="text-gray-600 font-medium">
                {faculty.specialization}
              </p>

              <p className="text-gray-500 mt-4 text-sm leading-relaxed">
                {faculty.bio}
              </p>

              <div className="mt-6 text-emerald-600 font-semibold">
                View Profile →
              </div>
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
