import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import { askQuestion } from "../api";

const SUGGESTED_QUESTIONS = [
  "Summarize this report's overall financial performance",
  "What was total revenue this quarter?",
  "How does revenue compare to the prior year?",
  "What did management say about the outlook?",
  "What are the key risk factors mentioned?",
];

export default function ChatWindow({ reportLoaded }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function sendMessage(text) {
    const question = (text ?? input).trim();
    if (!question || loading) return;

    setMessages((prev) => [...prev, { role: "user", text: question }]);
    setInput("");
    setLoading(true);

    try {
      const { answer } = await askQuestion(question);
      setMessages((prev) => [...prev, { role: "assistant", text: answer }]);
    } catch (err) {
      const detail =
        err?.response?.data?.detail || err.message || "Something went wrong.";
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: `⚠️ ${detail}` },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(e) {
    e.preventDefault();
    sendMessage();
  }

  if (!reportLoaded) {
    return (
      <div className="empty-state">
        <p>Upload and process a PDF report to start chatting.</p>
      </div>
    );
  }

  return (
    <div className="chat-window">
      <div className="messages">
        {messages.length === 0 && (
          <div className="suggestions">
            <p>Try asking</p>
            <ul>
              {SUGGESTED_QUESTIONS.map((q) => (
                <li key={q}>
                  <button className="suggestion-chip" onClick={() => sendMessage(q)}>
                    {q}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )}

        {messages.map((m, i) => (
          <div key={i} className={`message ${m.role}`}>
            {m.role === "assistant" && <div className="avatar">📊</div>}
            <div className="bubble">
              <ReactMarkdown>{m.text}</ReactMarkdown>
            </div>
          </div>
        ))}

        {loading && (
          <div className="message assistant">
            <div className="avatar">📊</div>
            <div className="bubble typing">Analyzing report...</div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <form className="input-row" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Ask about revenue, profit, trends, risks..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
        />
        <button type="submit" className="primary-btn" disabled={loading || !input.trim()}>
          ↑
        </button>
      </form>
    </div>
  );
}