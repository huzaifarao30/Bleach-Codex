import { api } from "../services/api";
import { useFetch } from "../hooks/useFetch";
import TimelineEntry from "../components/foreshadowing/TimelineEntry";
import PageTransition from "../animations/PageTransition";
import LoadingScreen from "../components/shared/LoadingScreen";

export default function Foreshadowing() {
  const { data, loading, error } = useFetch(() => api.listLoreEvents(), []);

  const entries = (data || []).filter(
    (e) => e.event_type === "foreshadowing_hint" || e.event_type === "payoff"
  );

  // Hints first, then their payoffs — reading order matches story order.
  entries.sort((a) => (a.event_type === "foreshadowing_hint" ? -1 : 1));

  return (
    <PageTransition>
      <h1 className="page-title">Foreshadowing → Payoff</h1>
      <p className="page-sub">
        Early hints traced forward to the reveals they set up, every link backed by a
        chapter citation, visible inline.
      </p>

      {loading && <LoadingScreen label="Reading between the lines…" />}
      {error && <div className="state-msg error">Couldn't load the timeline. Is the API running?</div>}
      {!loading && entries.length === 0 && (
        <div className="coming-soon">
          <div className="eyebrow">Coming Soon</div>
          <p>
            The first foreshadowing → payoff pair is being written now, tracing an
            early hint through to its reveal later in the arc. Check back shortly.
          </p>
        </div>
      )}
      <div className="timeline">
        {entries.map((e) => (
          <TimelineEntry key={e._id} event={e} />
        ))}
      </div>
    </PageTransition>
  );
}