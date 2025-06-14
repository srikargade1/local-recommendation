function LabeledInput({ label, value, onChange, type = "text", required = false }) {
  return (
    <div style={{ marginBottom: "1rem" }}>
      <label>{label}:</label><br />
      <input
        type={type}
        value={value}
        onChange={onChange}
        required={required}
      />
    </div>
  );
}

export default LabeledInput;
