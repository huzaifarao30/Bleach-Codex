import { Link } from "react-router-dom";
import { motion, useReducedMotion } from "framer-motion";

export default function CharacterCard({ character, index = 0 }) {
  const reduce = useReducedMotion();
  const hasPortrait = !!character.portrait_filename;

  return (
    <motion.div
      initial={reduce ? { opacity: 0 } : { opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.06, ease: "easeOut" }}
      whileHover={reduce ? undefined : { y: -4 }}
    >
      <Link
        to={`/characters/${character._id}`}
        className={`character-card${hasPortrait ? " has-portrait" : ""}`}
      >
        {hasPortrait && (
          <div className="card-portrait">
            <img
              src={`/assets/characters/${character.portrait_filename}`}
              alt=""
              onError={(e) => { e.currentTarget.parentElement.style.display = "none"; }}
            />
          </div>
        )}
        <h3>{character.name}</h3>
        <p>{character.biography}</p>
      </Link>
    </motion.div>
  );
}