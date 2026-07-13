import { motion, useReducedMotion } from "framer-motion";

/**
 * The signature "release" reveal: a brief gold flash on first view
 * (stronger for Bankai), settling into a static card.
 */
export default function PowerReleaseCard({ power, index = 0 }) {
  const reduce = useReducedMotion();
  const typeLabel = power.power_type === "other" && power.other_type_label
    ? power.other_type_label
    : power.power_type;

  return (
    <motion.div
      className={`power-card type-${power.power_type}`}
      initial={reduce ? { opacity: 0 } : { opacity: 0, scale: 0.97 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true, margin: "-40px" }}
      transition={{ duration: 0.45, delay: index * 0.08, ease: "easeOut" }}
    >
      {!reduce && (
        <motion.div
          className="release-flash"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: [0, 1, 0] }}
          viewport={{ once: true, margin: "-40px" }}
          transition={{ duration: 0.9, delay: index * 0.08, times: [0, 0.25, 1] }}
        />
      )}
      <div className="power-type">{typeLabel}</div>
      {power.image_filename && (
        <div className="power-image">
          <img
            src={`/assets/powers/${power.image_filename}`}
            alt=""
            onError={(e) => { e.currentTarget.parentElement.style.display = "none"; }}
          />
        </div>
      )}
      <div className="power-body">{power.ability_description}</div>
      {power.rules_and_limitations && (
        <div className="power-rules">
          <strong>Rules & limitations — </strong>
          {power.rules_and_limitations}
        </div>
      )}
      {power.evolution_notes && (
        <div className="power-rules">
          <strong>Evolution — </strong>
          {power.evolution_notes}
        </div>
      )}
    </motion.div>
  );
}