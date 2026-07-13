import { Link } from "react-router-dom";
import { api } from "../services/api";
import { useFetch } from "../hooks/useFetch";
import PowerReleaseCard from "../components/power/PowerReleaseCard";
import PageTransition from "../animations/PageTransition";
import LoadingScreen from "../components/shared/LoadingScreen";

export default function Powers() {
  const powersFetch = useFetch(() => api.listPowers(), []);
  const charactersFetch = useFetch(() => api.listCharacters(), []);

  const loading = powersFetch.loading || charactersFetch.loading;
  const error = powersFetch.error || charactersFetch.error;
  const powers = powersFetch.data;
  const characterById = {};
  (charactersFetch.data || []).forEach((c) => { characterById[c._id] = c; });

  return (
    <PageTransition>
      <h1 className="page-title">Powers</h1>
      <p className="page-sub">
        Every recorded ability across every character in the slice, each entry carries
        its canon rules and how it evolves later in the story.
      </p>

      {loading && <LoadingScreen label="Releasing…" />}
      {error && <div className="state-msg error">Couldn't load powers. Is the API running?</div>}
      {powers && powers.length === 0 && (
        <div className="state-msg">No powers recorded yet. Run the seed script.</div>
      )}
      {powers &&
        powers.map((p, i) => {
          const owner = characterById[p.character_id];
          return (
            <div key={p._id}>
              {owner && (
                <Link
                  to={`/characters/${owner._id}`}
                  style={{ fontSize: "0.72rem", color: "var(--soul)", letterSpacing: "0.08em", textTransform: "uppercase" }}
                >
                  {owner.name} →
                </Link>
              )}
              <PowerReleaseCard power={p} index={i} />
            </div>
          );
        })}
    </PageTransition>
  );
}