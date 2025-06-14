import React, { useState } from "react";
import Header from "./Components/Header";
import SearchForm from "./Components/SearchForm";
import PlaceList from "./Components/PlaceList";
import "./App.css";
import { useEffect } from "react";

function App() {
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

  useEffect(() => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLat(position.coords.latitude.toFixed(6));
        setLon(position.coords.longitude.toFixed(6));
        console.log("📍 Location set from browser");
      },
      (err) => {
        console.warn("⚠️ Could not get location:", err.message);
      }
        );
      }
    }, []);


  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResults([]);
    try {
      const res = await fetch("http://localhost:5000/places", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            prompt,
            lat: parseFloat(lat),
            lon: parseFloat(lon),
            gmaps_api_key: process.env.REACT_APP_GMAPS_API_KEY,
            max_walk_minutes: maxWalk ? parseInt(maxWalk) : null,
            max_drive_minutes: maxDrive ? parseInt(maxDrive) : null,
            exclude_chains: excludeChains,
            must_be_open: mustBeOpen,
            radius_meters: radiusMeters ? parseInt(radiusMeters) : 1000
        }),
      });
      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
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
/>

      <PlaceList results={results} loading={loading} />
    </div>
  );
}

export default App;
