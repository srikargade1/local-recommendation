import React, { useState, useEffect } from "react";
import Header from "./Components/Header";
import SearchForm from "./Components/SearchForm";
import PlaceList from "./Components/PlaceList";
import "./App.css";

const API_URL = process.env.REACT_APP_API_URL || "https://backend-wegy.onrender.com";

function App() {
  const [apiKey, setApiKey] = useState("");
  const [prompt, setPrompt] = useState("");
  const [lat, setLat] = useState("");
  const [lon, setLon] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [maxWalk, setMaxWalk] = useState("");
  const [maxDrive, setMaxDrive] = useState("");
  const [excludeChains, setExcludeChains] = useState(false);
  const [mustBeOpen, setMustBeOpen] = useState(false);
  const [radiusMeters, setRadiusMeters] = useState("1000");
  const [conversationHistory, setConversationHistory] = useState([]);
  const [refinePrompt, setRefinePrompt] = useState("");

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLat(position.coords.latitude.toFixed(6));
          setLon(position.coords.longitude.toFixed(6));
          console.log("📍 Location set from browser");
        },
        (err) => console.warn("⚠️ Could not get location:", err.message)
      );
    }
  }, []);

  const submitSearch = async (searchPrompt, history) => {
    setLoading(true);
    setResults([]);
    try {
      const res = await fetch(`${API_URL}/places`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt: searchPrompt,
          lat: parseFloat(lat),
          lon: parseFloat(lon),
          gmaps_api_key: apiKey,
          max_walk_minutes: maxWalk ? parseInt(maxWalk) : null,
          max_drive_minutes: maxDrive ? parseInt(maxDrive) : null,
          exclude_chains: excludeChains,
          must_be_open: mustBeOpen,
          radius_meters: radiusMeters ? parseInt(radiusMeters) : 1000,
          conversation_history: history,
        }),
      });
      const data = await res.json();
      setResults(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Fresh search — clears conversation history
  const handleSubmit = async (e) => {
    e.preventDefault();
    const freshHistory = [];
    setConversationHistory(freshHistory);
    await submitSearch(prompt, freshHistory);
  };

  // Refinement — builds on prior results using conversation history
  const handleRefine = async (e) => {
    e.preventDefault();
    if (!refinePrompt.trim()) return;

    const updatedHistory = [
      ...conversationHistory,
      { role: "user", content: prompt },
      { role: "assistant", content: `Found ${results.length} places near the user.` },
    ];

    setConversationHistory(updatedHistory);
    setPrompt(refinePrompt);
    setRefinePrompt("");
    await submitSearch(refinePrompt, updatedHistory);
  };

  // Sends thumbs up/down to the backend feedback log
  const handleFeedback = async (place, thumbsUp) => {
    try {
      await fetch(`${API_URL}/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          fsq_id: place.fsq_id,
          place_name: place.name,
          query: prompt,
          thumbs_up: thumbsUp,
        }),
      });
    } catch (err) {
      console.error("Feedback error:", err);
    }
  };

  return (
    <div className="app-wrapper">
      <Header />
      <SearchForm
        prompt={prompt}
        lat={lat}
        lon={lon}
        setPrompt={setPrompt}
        setLat={setLat}
        setLon={setLon}
        handleSubmit={handleSubmit}
        loading={loading}
        maxWalk={maxWalk}
        setMaxWalk={setMaxWalk}
        maxDrive={maxDrive}
        setMaxDrive={setMaxDrive}
        excludeChains={excludeChains}
        setExcludeChains={setExcludeChains}
        mustBeOpen={mustBeOpen}
        setMustBeOpen={setMustBeOpen}
        radiusMeters={radiusMeters}
        setRadiusMeters={setRadiusMeters}
        apiKey={apiKey}
        setApiKey={setApiKey}
      />

      {results.length > 0 && !loading && (
        <form onSubmit={handleRefine} className="refine-form">
          <input
            type="text"
            value={refinePrompt}
            onChange={(e) => setRefinePrompt(e.target.value)}
            placeholder="Refine your search... e.g. 'something quieter' or 'closer to me'"
          />
          <button type="submit">Refine</button>
        </form>
      )}

      <PlaceList results={results} loading={loading} onFeedback={handleFeedback} />
    </div>
  );
}

export default App;
