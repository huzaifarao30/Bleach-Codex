import { Link } from "react-router-dom";
import { motion, useReducedMotion } from "framer-motion";
import PageTransition from "../animations/PageTransition";

// Set this to the exact filename of your hero art, dropped into
// frontend/public/assets/hero/ — check with `dir`/`ls` for the real
// extension before assuming .png.
const HERO_IMAGE = "hero_pic-removebg-preview.png";

export default function Landing() {
  const reduce = useReducedMotion();

  return (
    <PageTransition>
      <div className="landing-hero">
        <div className="landing-copy">
          <div className="eyebrow">Vertical Slice, Kurosaki Family · Soul Society Arc</div>
          <motion.h1
            initial={reduce ? { opacity: 0 } : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
          >
            The lore, <em>grounded.</em>
          </motion.h1>
          <p>
            Bleach Codex is a structured encyclopedia that reasons across the story
            instead of just displaying it, every character, power, and reveal traced
            back to its source chapter. Explore the Kurosaki family tree, trace
            foreshadowing to its payoff, and see exactly where the story keeps its
            promises.
          </p>
          <Link to="/characters" className="landing-cta">
            Enter the Codex
          </Link>
        </div>

        <div className="hero-portrait-wrap">
          <motion.div
            className="hero-portrait-clip"
            initial={reduce ? { opacity: 0 } : { clipPath: "inset(0 100% 0 0)" }}
            animate={{ clipPath: "inset(0 0% 0 0)", opacity: 1 }}
            transition={{ duration: 0.7, delay: 0.15, ease: [0.7, 0, 0.2, 1] }}
          >
            <img
              src={`/assets/hero/${HERO_IMAGE}`}
              alt="Ichigo Kurosaki, mid-release"
              onError={(e) => { e.currentTarget.parentElement.style.display = "none"; }}
            />
          </motion.div>

          {!reduce && (
            <svg className="hero-slash" viewBox="0 0 380 507" preserveAspectRatio="none">
              <motion.line
                x1="-20" y1="530" x2="400" y2="-20"
                stroke="var(--gold)"
                strokeWidth="6"
                initial={{ pathLength: 0, opacity: 1 }}
                animate={{ pathLength: 1, opacity: [1, 1, 0] }}
                transition={{ duration: 0.45, delay: 0.05, times: [0, 0.7, 1] }}
              />
            </svg>
          )}
        </div>
      </div>

    </PageTransition>
  );
}