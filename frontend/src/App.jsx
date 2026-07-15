import { useEffect, useState } from "react";
import FileUpload from "./components/FileUpload.jsx";
import ChatWindow from "./components/ChatWindow.jsx";
import IconRail from "./components/IconRail.jsx";
import { getStatus, resetMemory } from "./api";
import "./App.css";

export default function App() {
  const [status, setStatus] = useState({
    report_loaded: false,
    filename: null,
    num_chunks: 0,
  });
  const [chatKey, setChatKey] = useState(0);
  const [history, setHistory] = useState([]); // list of previously loaded report names

  useEffect(() => {
    getStatus()
      .then(setStatus)
      .catch(() => {});
  }, []);

  function handleUploaded(result) {
    setStatus({
      report_loaded: true,
      filename: result.filename,
      num_chunks: result.num_chunks,
    });
    setHistory((prev) => [
      { name: result.filename, chunks: result.num_chunks },
      ...prev.filter((h) => h.name !== result.filename),
    ]);
    setChatKey((k) => k + 1);
  }

  async function handleClearMemory() {
    await resetMemory();
    setChatKey((k) => k + 1);
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>📊 Financial Report Analyst</h1>
        <p>
          Upload a quarterly earnings report or 10-Q/10-K PDF and ask
          questions about revenue, profitability, trends, and key metrics —
          powered by Groq's Llama&nbsp;3.
        </p>
      </header>

      <div className="app-body">
        <aside className="sidebar">
          <FileUpload onUploaded={handleUploaded} disabled={false} />

          {status.report_loaded && (
            <div className="status-card">
              <h3>Loaded report</h3>
              <p className="filename">{status.filename}</p>
              <p className="chunk-count">{status.num_chunks} chunks indexed</p>
              <button className="secondary-btn" onClick={handleClearMemory}>
                Clear conversation memory
              </button>
            </div>
          )}

          {history.length > 0 && (
            <div className="status-card">
              <h3>Report history</h3>
              <ul className="history-list">
                {history.map((h) => (
                  <li key={h.name} className="history-item">
                    {h.name}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </aside>

        <main className="main-panel">
          <ChatWindow key={chatKey} reportLoaded={status.report_loaded} />
        </main>

        <IconRail />
      </div>
    </div>
  );
}