import PlaceCard from "./PlaceCard";

function PlaceList({ results, loading, onFeedback }) {
  if (loading) return <p className="loading">Finding the best places for you...</p>;
  if (!results.length) return <p className="empty">No results found. Try adjusting your search.</p>;

  return (
    <section className="results">
      <h2>Recommendations <span className="result-count">({results.length})</span></h2>
      {results.map(place => (
        <PlaceCard key={place.fsq_id} place={place} onFeedback={onFeedback} />
      ))}
    </section>
  );
}

export default PlaceList;
