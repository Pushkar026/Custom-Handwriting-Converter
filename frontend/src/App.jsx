import { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [font, setFont] = useState("neat");
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  const uploadTextAndConvert = async () => {
    if (!text.trim()) {
      alert("Please enter some text");
      return;
    }

    try {
      setLoading(true);
      setImageUrl(null);

      const uploadRes = await fetch(
        "http://127.0.0.1:8000/api/upload/text",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text }),
        }
      );

      const uploadData = await uploadRes.json();
      const fileId = uploadData.file_id;

      const convertRes = await fetch(
        "http://127.0.0.1:8000/api/convert",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            file_id: fileId,
            file_type: "text",
            font_key: font,
          }),
        }
      );

      const convertData = await convertRes.json();

      setImageUrl(
        `http://127.0.0.1:8000/outputs/${convertData.output_id}.png`
      );
    } catch (err) {
      console.error(err);
      alert("Something went wrong. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1>Custom Handwriting Converter</h1>

      <textarea
        placeholder="Enter text to convert..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={6}
      />

      <select value={font} onChange={(e) => setFont(e.target.value)}>
  <option value="handwriting">Handwriting</option>
  <option value="calibri">Calibri</option>
  <option value="arial">Arial</option>
  <option value="palscript">Pal Script</option>
  <option value="chiller">Chiller</option>
  <option value="rage">Rage</option>
</select>


      <button onClick={uploadTextAndConvert} disabled={loading}>
        {loading ? "Converting..." : "Convert to Handwriting"}
      </button>

      {imageUrl && (
        <div className="output">
          <h2>Result</h2>
          <img src={imageUrl} alt="Handwritten Output" />
          <a href={imageUrl} download>
            Download Image
          </a>
        </div>
      )}
    </div>
  );
}

export default App;


