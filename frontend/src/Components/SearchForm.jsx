import React from "react";

function SearchForm({
  prompt,
  lat,
  lon,
  setPrompt,
  setLat,
  setLon,
  handleSubmit,
  loading,
  maxWalk,
  setMaxWalk,
  maxDrive,
  setMaxDrive,
  excludeChains,
  setExcludeChains,
  mustBeOpen,
  setMustBeOpen,
  radiusMeters,
  setRadiusMeters,
  apiKey,
  setApiKey
}) {
  return (
    <form onSubmit={handleSubmit} className="search-form">
      <div>
        <label>
          Google Maps API Key:
          <input
            type="text"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="Enter your Google Maps API key"
          />
        </label>
      </div>

      <div>
        <label>
          What are you looking for?
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g., cafe, bookstore"
          />
        </label>
      </div>

      <div className="latlon-row">
        <label>
          Latitude:
          <input
            type="text"
            value={lat}
            onChange={(e) => setLat(e.target.value)}
            placeholder="e.g., 43.04"
          />
        </label>
        <label>
          Longitude:
          <input
            type="text"
            value={lon}
            onChange={(e) => setLon(e.target.value)}
            placeholder="e.g., -76.12"
          />
        </label>
        <div className="radius-group">
          <label htmlFor="radius-input">
            Search Radius (meters)
          </label>
          <select
            id="radius-select"
            value={radiusMeters}
            onChange={(e) => setRadiusMeters(e.target.value)}
          >
            <option value="500">500 m</option>
            <option value="1000">1000 m</option>
            <option value="2000">2000 m</option>
            <option value="3000">3000 m</option>
            <option value="5000">5000 m</option>
          </select>
        </div>
      </div>

      <div className="filters-row">
        <div className="filter-group">
          <label>
            Max Walk Time (min):
            <input
              type="number"
              value={maxWalk}
              onChange={(e) => setMaxWalk(e.target.value)}
              placeholder="e.g., 10"
            />
          </label>
        </div>

        <div className="filter-group">
          <label>
            Max Drive Time (min):
            <input
              type="number"
              value={maxDrive}
              onChange={(e) => setMaxDrive(e.target.value)}
              placeholder="e.g., 5"
            />
          </label>
        </div>

        <div className="filter-checkboxes">
          <label>
            <input
              type="checkbox"
              checked={excludeChains}
              onChange={(e) => setExcludeChains(e.target.checked)}
            />
            Exclude Chains
          </label>
          <label>
            <input
              type="checkbox"
              checked={mustBeOpen}
              onChange={(e) => setMustBeOpen(e.target.checked)}
            />
            Must Be Open
          </label>
        </div>
      </div>

      <button type="submit" disabled={loading}>
        {loading ? "Searching..." : "Search"}
      </button>
    </form>
  );
}

export default SearchForm;
