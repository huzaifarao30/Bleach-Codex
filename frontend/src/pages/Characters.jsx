import { api } from "../services/api";
import { useFetch } from "../hooks/useFetch";
import CharacterCard from "../components/character/CharacterCard";
import PageTransition from "../animations/PageTransition";
import LoadingScreen from "../components/shared/LoadingScreen";

export default function Characters() {
  const { data, loading, error } = useFetch(() => api.listCharacters(), []);

  return (
    <PageTransition>
      <h1 className="page-title">Characters</h1>
      <p className="page-sub">
        Every figure in the current slice. Select a character to open their full record.
      </p>

      {loading && <LoadingScreen label="Opening the archive…" />}
      {error && (
        <div className="state-msg error">
          Couldn't reach the Codex API. Check that the backend is running, then reload.
        </div>
      )}
      {data && data.length === 0 && (
        <div className="state-msg">
          The archive is empty. Run the seed script to populate it.
        </div>
      )}
      {data && (
        <div className="card-grid">
          {data.map((c, i) => (
            <CharacterCard key={c._id} character={c} index={i} />
          ))}
        </div>
      )}
    </PageTransition>
  );
}