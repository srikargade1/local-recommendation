function PlaceCard({ place }) {
  const { travel_info } = place;

  return (
    <div className="place-card">
      <h3>{place.name}</h3>
      <p className="address">{place.address}</p>

      {travel_info && (
        <div className="travel-info">
          <p><strong>🚶 Walking:</strong> {travel_info.walking?.duration_text || 'N/A'}</p>
          <p><strong>🚗 Driving:</strong> {travel_info.driving?.duration_text || 'N/A'}</p>
          <p><strong>🚌 Transit:</strong> {travel_info.transit?.duration_text || 'N/A'}</p>
        </div>
      )}

      <a href={place.directions_link} target="_blank" rel="noreferrer">
        Get Directions →
      </a>
    </div>
  );
}
export default PlaceCard;

