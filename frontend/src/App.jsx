import { useState } from "react";
import {
  Send,
  Sparkles,
  Trash2,
  MessageSquare,
  LoaderCircle,
} from "lucide-react";

import "./App.css";

const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:5000/api";

function App() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const askQuestion = async () => {
    if (!question.trim() || loading) return;

    setLoading(true);
    setError("");
    setResponse("");

    try {
      const res = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userInput: question.trim(),
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || "Something went wrong");
      }

      setResponse(data.response);
    } catch (err) {
      setError(err.message || "Failed to connect to the server");
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    setQuestion("");
    setResponse("");
    setError("");
  };

  return (
    <div className="app">
      <header className="header">
        <div className="brand">
          <div className="brand-icon">
            <Sparkles size={22} />
          </div>

          <div>
            <h1>EduAI</h1>
            <p>AI-powered education assistant</p>
          </div>
        </div>

        <button className="clear-button" onClick={clearChat}>
          <Trash2 size={17} />
          Clear
        </button>
      </header>

      <main className="main">
        <section className="hero">
          <div className="hero-icon">
            <Sparkles size={30} />
          </div>

          <h2>Ask anything about education</h2>

          <p>
            Get clear, helpful answers powered by AI.
          </p>
        </section>

        <section className="chat-card">
          <div className="input-header">
            <MessageSquare size={18} />
            <span>Your question</span>
          </div>

          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                askQuestion();
              }
            }}
            placeholder="Ask a question..."
            rows={5}
          />

          <div className="input-footer">
            <span>Press Enter to send</span>

            <button
              className="send-button"
              onClick={askQuestion}
              disabled={!question.trim() || loading}
            >
              {loading ? (
                <>
                  <LoaderCircle className="spin" size={18} />
                  Thinking...
                </>
              ) : (
                <>
                  <Send size={18} />
                  Ask AI
                </>
              )}
            </button>
          </div>
        </section>

        {error && (
          <div className="error">
            {error}
          </div>
        )}

        {response && (
          <section className="response-card">
            <div className="response-header">
              <div className="response-title">
                <Sparkles size={18} />
                <span>AI Response</span>
              </div>
            </div>

            <div className="response-content">
              {response}
            </div>
          </section>
        )}
      </main>

      <footer>
        <span>EduAI</span>
        <span>•</span>
        <span>Powered by Groq</span>
      </footer>
    </div>
  );
}

export default App;