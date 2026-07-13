import { motion, useReducedMotion } from "framer-motion";
import SourceCitationChip from "./SourceCitationChip";

const KIND_LABEL = {
  foreshadowing_hint: "Foreshadowing",
  payoff: "Payoff",
  contradiction: "Contradiction",
};

/** Scroll-triggered reveal: slides/fades in as it enters the viewport. */
export default function TimelineEntry({ event }) {
  const reduce = useReducedMotion();
  const isPayoff = event.event_type === "payoff";

  return (
    <motion.div
      className={`timeline-entry${isPayoff ? " payoff" : ""}`}
      initial={reduce ? { opacity: 0 } : { opacity: 0, x: -18 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true, margin: "-60px" }}
      transition={{ duration: 0.5, ease: "easeOut" }}
    >
      <div className="entry-kind">{KIND_LABEL[event.event_type] || event.event_type}</div>
      <p style={{ fontSize: "0.88rem" }}>{event.description}</p>
      <div>
        {(event.sources || []).map((s) => (
          <SourceCitationChip key={s._id} source={s} />
        ))}
      </div>
    </motion.div>
  );
}