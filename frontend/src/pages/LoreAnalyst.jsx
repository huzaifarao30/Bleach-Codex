import { useState } from "react";
import { api } from "../services/api";
import PageTransition from "../animations/PageTransition";
import LoadingScreen from "../components/shared/LoadingScreen";

/**
 * The real Lore Analyst. Gates on a spoiler boundary before any question can
 * be asked, then calls the actual RAG-backed /lore-analyst/query endpoint.
 * If the backend has no Gemini API key configured, this shows that plainly
 * rather than pretending to work.
 */
export default function LoreAnalyst() {
  const [progress, setProgress] = useState(null);
  const [draft, setDraft] = useState("");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAsk = async () => {
    if (!question.trim() || loading) return;
    const asked = question.trim();
    setMessages((m) => [...m, { role: "user", text: asked }]);
    setQuestion("");
    setLoading(true);
    setError(null);
    try {
      const result = await api.askLoreAnalyst(asked, progress);
      setMessages((m) => [...m, { role: "analyst", text: result.answer, sources: result.sources }]);
    } catch (e) {
      if (e.status === 503) {
        setError("The Analyst's backend isn't fully configured yet — it needs a Gemini API key set on the server before it can answer anything.");
      } else {
        setError("Couldn't reach the Analyst. Check that the backend is running, then try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  if (!progress) {
    return (
      <PageTransition>
        <h1 className="page-title">Lore Analyst</h1>
        <p className="page-sub">
          Before anything else — how far have you gotten? Every answer the Analyst
          gives will stay within that point. Nothing past it, ever, even if you ask
          directly.
        </p>

        <div className="analyst-shell">
          <div className="profile-field" style={{ marginBottom: 16 }}>
            <span className="label">I've watched up to episode / read up to chapter</span>
            <input
              type="text"
              value={draft}
              onChange={(e) => setDraft(e.target.value)}
              placeholder="e.g. Episode 109 / Chapter 184 (end of Soul Society Arc)"
              style={{
                width: "100%", marginTop: 8, background: "var(--void)", border: "var(--edge)",
                borderRadius: "var(--radius)", color: "var(--text)", padding: "10px 14px",
                fontFamily: "var(--font-body)", fontSize: "0.88rem",
              }}
            />
          </div>
          <button
            className="landing-cta"
            style={{ border: "1px solid var(--gold)", background: "none" }}
            disabled={!draft.trim()}
            onClick={() => setProgress(draft.trim())}
          >
            Set my progress
          </button>
        </div>
      </PageTransition>
    );
  }

  return (
    <PageTransition>
      <h1 className="page-title">Lore Analyst</h1>
      <p className="page-sub">
        Spoiler boundary set at <strong style={{ color: "var(--gold)" }}>{progress}</strong>.{" "}
        <button
          onClick={() => { setProgress(null); setMessages([]); }}
          style={{ background: "none", border: "none", color: "var(--soul)", textDecoration: "underline", cursor: "pointer", padding: 0, fontSize: "inherit" }}
        >
          Change this
        </button>
      </p>

      <div className="analyst-shell">
        {messages.length === 0 && !loading && (
          <div className="analyst-msg">
            Ask anything about the story up to your stated point. When the Codex has real
            data on it, answers are grounded and cite their source. When it doesn't, the
            Analyst can still answer from general Bleach knowledge — clearly labeled as
            such so you always know which kind of answer you're getting. Either way,
            nothing past your spoiler boundary gets discussed.
          </div>
        )}

        {messages.map((m, i) => (
          <div
            key={i}
            className="analyst-msg"
            style={m.role === "user" ? { borderColor: "rgba(212, 175, 47, 0.4)" } : undefined}
          >
            <div style={{ fontSize: "0.68rem", letterSpacing: "0.12em", textTransform: "uppercase", color: m.role === "user" ? "var(--gold)" : "var(--soul)", marginBottom: 6 }}>
              {m.role === "user" ? "You" : "Analyst"}
            </div>
            {m.text}
            {m.sources && m.sources.length > 0 && (
              <div style={{ marginTop: 10 }}>
                {m.sources.map((s, si) => (
                  <span key={si} className="source-chip">{s.name}</span>
                ))}
              </div>
            )}
          </div>
        ))}

        {loading && <LoadingScreen label="Consulting the records…" />}
        {error && <div className="state-msg error" style={{ padding: "12px 0" }}>{error}</div>}

        <div className="analyst-input-row">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter") handleAsk(); }}
            placeholder="e.g. Why did Ichigo's Bankai only take three days?"
            disabled={loading}
            aria-label="Ask the Lore Analyst"
          />
          <button onClick={handleAsk} disabled={loading || !question.trim()}>
            Ask
          </button>
        </div>
      </div>
    </PageTransition>
  );
}