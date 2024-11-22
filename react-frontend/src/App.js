import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [url, setUrl] = useState("");
  const [responseData, setResponseData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/scrape/", { url });
      setResponseData(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Web Scraper and Instagram Image Extractor</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Scraping..." : "Submit"}
        </button>
      </form>

      {error && <div style={{ color: "red" }}>Error: {error}</div>}

      {responseData && (
        <div>
          <h2>Scraped Data:</h2>
          <h3>Images:</h3>
          {responseData.images.length > 0 ? (
            responseData.images.map((img, index) => (
              <img key={index} src={img} alt={`Scraped Image ${index}`} width="200" />
            ))
          ) : (
            <p>No images found.</p>
          )}
          <h3>Text:</h3>
          <p>{responseData.texts || "No text found."}</p>
          <h3>Generated Text:</h3>
          <p>{responseData.generated_text || "No generated text."}</p>
        </div>
      )}
    </div>
  );
};

export default App;
