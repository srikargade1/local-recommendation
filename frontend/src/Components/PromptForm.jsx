import LabeledInput from './LabelledInput';

function PromptForm({ prompt, lat, lon, setPrompt, setLat, setLon, onSubmit, loading }) {
  return (
    <form onSubmit={onSubmit}>
      <LabeledInput
        label="User Prompt"
        value={prompt}
        onChange={e => setPrompt(e.target.value)}
        required
      />
      <LabeledInput
        label="Latitude"
        value={lat}
        onChange={e => setLat(e.target.value)}
        required
      />
      <LabeledInput
        label="Longitude"
        value={lon}
        onChange={e => setLon(e.target.value)}
        required
      />
      <button type="submit" disabled={loading}>Search</button>
    </form>
  );
}

export default PromptForm;
