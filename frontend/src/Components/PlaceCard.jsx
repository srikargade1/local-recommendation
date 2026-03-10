import { useState } from "react";

function PlaceCard({ place, onFeedback }) {
  const { travel_info } = place;
  const [feedbackGiven, setFeedbackGiven] = useState(null);

  const handleFeedback = (thumbsUp) => {
    setFeedbackGiven(thumbsUp ? "up" : "down");
    if (onFeedback) onFeedback(place, thumbsUp);
  };

  return (
    <div className="place-card">
      {place.photo_url && (
        <img
          src={place.photo_url}
          alt={place.name}
          className="place-photo"
          onError={(e) => { e.target.style.display = "none"; }}
        />
      )}

      <div className="place-card-body">
        <div className="place-card-header">
          <h3>{place.name}</h3>
          {place.is_open_now !== undefined && (
            <span className={`open-badge ${place.is_open_now ? "open" : "closed"}`}>
              {place.is_open_now ? "Open" : "Closed"}
            </span>
          )}
        </div>

        {place.categories?.length > 0 && (
          <p className="categories">{place.categories.join(" · ")}</p>
        )}

        <p className="address">{place.address}</p>

        {place.explanation && (
          <p className="explanation">✨ {place.explanation}</p>
        )}

        {travel_info && (
          <div className="travel-info">
            <span>🚶 {travel_info.walking?.duration_text || "N/A"}</span>
            <span>🚗 {travel_info.driving?.duration_text || "N/A"}</span>
            <span>🚌 {travel_info.transit?.duration_text || "N/A"}</span>
          </div>
        )}

        <div className="card-footer">
          <a href={place.directions_link} target="_blank" rel="noreferrer">
            Get Directions →
          </a>

          <div className="feedback-buttons">
            {feedbackGiven ? (
              <span className="feedback-thanks">Thanks!</span>
            ) : (
              <>
                <button
                  className="feedback-btn"
                  title="Relevant result"
                  onClick={() => handleFeedback(true)}
                >👍</button>
                <button
                  className="feedback-btn"
                  title="Not relevant"
                  onClick={() => handleFeedback(false)}
                >👎</button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default PlaceCard;
