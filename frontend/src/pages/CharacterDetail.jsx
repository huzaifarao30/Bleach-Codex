import { useParams, Link } from "react-router-dom";
import { motion, useReducedMotion } from "framer-motion";
import { api } from "../services/api";
import { useFetch } from "../hooks/useFetch";
import PowerReleaseCard from "../components/power/PowerReleaseCard";
import RelationshipBadge from "../components/character/RelationshipBadge";
import PageTransition from "../animations/PageTransition";
import LoadingScreen from "../components/shared/LoadingScreen";

function Section({ title, children, delay = 0 }) {
  const reduce = useReducedMotion();
  return (
    <motion.section
      className="profile-section"
      initial={reduce ? { opacity: 0 } : { opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45, delay, ease: "easeOut" }}
    >
      <h2>{title}</h2>
      {children}
    </motion.section>
  );
}

export default function CharacterDetail() {
  const { id } = useParams();
  const { data, loading, error } = useFetch(() => api.getCharacterFull(id), [id]);

  if (loading) return <LoadingScreen label="Retrieving record…" />;
  if (error)
    return (
      <div className="state-msg error">
        Couldn't load this character. They may not exist, or the API is unreachable.
      </div>
    );
  if (!data) return null;

  return (
    <PageTransition>
      <header className="profile-header">
        <div className="eyebrow">Character Record</div>
        <h1 className="page-title" style={{ margin: "4px 0 0" }}>{data.name}</h1>
      </header>

      <div className="profile-layout">
        <div className="profile-main">
          <Section title="Profile" delay={0}>
            <div className="profile-field">
              <span className="label">Biography</span>
              {data.biography}
            </div>
            {data.personality && (
              <div className="profile-field">
                <span className="label">Personality</span>
                {data.personality}
              </div>
            )}
            {data.appearance && (
              <div className="profile-field">
                <span className="label">Appearance</span>
                {data.appearance}
              </div>
            )}
          </Section>

          <Section title="Powers" delay={0.08}>
            {data.powers.length === 0 ? (
              <div className="state-msg" style={{ padding: "8px 0" }}>
                No recorded powers for this character yet.
              </div>
            ) : (
              data.powers.map((p, i) => (
                <PowerReleaseCard key={p._id} power={p} index={i} />
              ))
            )}
          </Section>

          <Section title="Relationships" delay={0.16}>
            {data.relationships.length === 0 ? (
              <div className="state-msg" style={{ padding: "8px 0" }}>
                No recorded connections yet.
              </div>
            ) : (
              <div className="rel-list">
                {data.relationships.map((r) => (
                  <div className="rel-row" key={r.id}>
                    <RelationshipBadge type={r.relationship_type} />
                    <Link className="rel-name" to={`/characters/${r.other_character_id}`}>
                      {r.other_character_name}
                    </Link>
                    {r.plot_relevance_note && (
                      <div className="rel-note">{r.plot_relevance_note}</div>
                    )}
                  </div>
                ))}
              </div>
            )}
            <div style={{ marginTop: 18 }}>
              <Link to={`/family-tree/${data.id}`} className="landing-cta" style={{ fontSize: "0.75rem", padding: "9px 18px" }}>
                View in family tree
              </Link>
            </div>
          </Section>

          <Section title="Arc Appearances" delay={0.24}>
            {data.arcs.length === 0 ? (
              <div className="state-msg" style={{ padding: "8px 0" }}>
                No arc appearances linked yet.
              </div>
            ) : (
              data.arcs.map((a) => <div key={a.id}>{a.name}</div>)
            )}
          </Section>
        </div>

        <motion.div
          className="profile-portrait-panel"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          {data.full_body_filename ? (
            <img
              src={`/assets/characters/${data.full_body_filename}`}
              alt={`${data.name}, full body`}
              onError={(e) => {
                e.currentTarget.replaceWith(
                  Object.assign(document.createElement("div"), {
                    className: "profile-portrait-fallback",
                    textContent: "No portrait yet",
                  })
                );
              }}
            />
          ) : (
            <div className="profile-portrait-fallback">No portrait yet</div>
          )}
        </motion.div>
      </div>
    </PageTransition>
  );
}