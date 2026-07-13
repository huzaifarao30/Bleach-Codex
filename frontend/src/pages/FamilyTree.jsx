import { useParams, useNavigate } from "react-router-dom";
import { api } from "../services/api";
import { useFetch } from "../hooks/useFetch";
import FamilyTreeGraph from "../components/family-tree/FamilyTreeGraph";
import PageTransition from "../animations/PageTransition";
import LoadingScreen from "../components/shared/LoadingScreen";

export default function FamilyTree() {
  const { id } = useParams();
  const navigate = useNavigate();

  // If no character selected yet, load the list to offer a starting point.
  const characters = useFetch(() => api.listCharacters(), []);
  const tree = useFetch(
    () => (id ? api.getFamilyTree(id, 1) : Promise.resolve(null)),
    [id]
  );

  return (
    <PageTransition>
      <h1 className="page-title">Family Tree</h1>
      <p className="page-sub">
        Relationships as an explorable graph. Every connection label is shown from the
        centered character's perspective — click any node to re-center on them.
      </p>

      {!id && (
        <>
          {characters.loading && <LoadingScreen label="Loading characters…" />}
          {characters.data && (
            <div className="card-grid">
              {characters.data.map((c) => (
                <button
                  key={c._id}
                  className="character-card"
                  style={{ textAlign: "left", background: "var(--void-card)", border: "var(--edge)", color: "inherit" }}
                  onClick={() => navigate(`/family-tree/${c._id}`)}
                >
                  <h3>{c.name}</h3>
                  <p>Start the tree here</p>
                </button>
              ))}
            </div>
          )}
        </>
      )}

      {id && tree.loading && <LoadingScreen label="Tracing bloodlines…" />}
      {id && tree.error && (
        <div className="state-msg error">Couldn't load this tree — is the API running?</div>
      )}
      {id && tree.data && (
        <FamilyTreeGraph
          tree={tree.data}
          focusId={id}
          onFocus={(newId) => navigate(`/family-tree/${newId}`)}
        />
      )}
    </PageTransition>
  );
}