import PlaceCard from "./PlaceCard";

function PlaceList({ results, loading }) {
  console.log(results);
  if (loading) return null;
  if (!results.length) return <p className="empty">No results found.</p>;

  return (
    <section className="results">
      <h2>Recommendations</h2>
      {results.map(place => (
        <PlaceCard key={place.fsq_id} place={place} />
      ))}
    </section>
  );
}

export default PlaceList;
