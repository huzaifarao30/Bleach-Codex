import { motion, useReducedMotion } from "framer-motion";

/**
 * Custom SVG family tree: the focused character sits at center, connected
 * characters arranged in a ring around them. Clicking (or pressing Enter on)
 * any node re-centers the tree on that character. Edges draw in as animated
 * lines; labels show the relationship type exactly as the API resolved it.
 */
const W = 900;
const H = 560;
const CX = W / 2;
const CY = H / 2;
const RING_R = 195;

export default function FamilyTreeGraph({ tree, focusId, onFocus }) {
  const reduce = useReducedMotion();

  if (!tree || tree.nodes.length === 0) {
    return <div className="state-msg">No characters found in this tree.</div>;
  }

  const others = tree.nodes.filter((n) => n.id !== focusId);
  const focusNode = tree.nodes.find((n) => n.id === focusId);

  // Radial positions: focus at center, others evenly spaced on a ring.
  const positions = { [focusId]: { x: CX, y: CY } };
  others.forEach((n, i) => {
    const angle = (i / others.length) * Math.PI * 2 - Math.PI / 2;
    positions[n.id] = {
      x: CX + Math.cos(angle) * RING_R,
      y: CY + Math.sin(angle) * RING_R,
    };
  });

  // Multiple relationship rows can exist between the same two characters
  // (e.g. "enemy" AND "ally"). Drawing each as its own line stacks them
  // directly on top of each other, with labels overlapping illegibly.
  // Merge same-pair edges into one line with a combined label instead.
  const mergedEdges = [];
  const seenPairs = new Map();
  for (const e of tree.edges) {
    const pairKey = [e.from_character_id, e.to_character_id].sort().join("|");
    if (seenPairs.has(pairKey)) {
      const existing = mergedEdges[seenPairs.get(pairKey)];
      if (!existing.relationship_type.includes(e.relationship_type)) {
        existing.relationship_type += ` / ${e.relationship_type}`;
      }
    } else {
      seenPairs.set(pairKey, mergedEdges.length);
      mergedEdges.push({ ...e });
    }
  }

  // Only draw edges where both ends have a position (depth may exceed ring).
  const drawableEdges = mergedEdges.filter(
    (e) => positions[e.from_character_id] && positions[e.to_character_id]
  );

  return (
    <div className="tree-wrap">
      <svg className="tree-svg" viewBox={`0 0 ${W} ${H}`} role="group" aria-label="Family tree graph">
        <defs>
          {tree.nodes.map((n) => {
            const pos = positions[n.id];
            if (!pos || !n.portrait_filename) return null;
            const r = n.id === focusId ? 34 : 26;
            return (
              <clipPath id={`clip-${n.id}`} key={n.id}>
                <circle cx={pos.x} cy={pos.y} r={r} />
              </clipPath>
            );
          })}
        </defs>

        {drawableEdges.map((e, i) => {
          const a = positions[e.from_character_id];
          const b = positions[e.to_character_id];
          const midX = (a.x + b.x) / 2;
          const midY = (a.y + b.y) / 2;
          return (
            <g key={e.id}>
              <motion.line
                className="tree-edge"
                x1={a.x} y1={a.y} x2={b.x} y2={b.y}
                initial={reduce ? { opacity: 0 } : { pathLength: 0, opacity: 0 }}
                animate={{ pathLength: 1, opacity: 1 }}
                transition={{ duration: 0.5, delay: 0.15 + i * 0.06 }}
              />
              <motion.text
                className="tree-edge-label"
                x={midX} y={midY - 6}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3, delay: 0.4 + i * 0.06 }}
              >
                {e.relationship_type}
              </motion.text>
            </g>
          );
        })}

        {tree.nodes.map((n, i) => {
          const pos = positions[n.id];
          if (!pos) return null;
          const isFocus = n.id === focusId;
          return (
            <motion.g
              key={n.id}
              className={`tree-node${isFocus ? " focus" : ""}`}
              initial={reduce ? { opacity: 0 } : { opacity: 0, scale: 0.6 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ type: "spring", stiffness: 220, damping: 20, delay: i * 0.05 }}
              style={{ transformOrigin: `${pos.x}px ${pos.y}px` }}
              onClick={() => !isFocus && onFocus(n.id)}
              onKeyDown={(ev) => {
                if ((ev.key === "Enter" || ev.key === " ") && !isFocus) {
                  ev.preventDefault();
                  onFocus(n.id);
                }
              }}
              tabIndex={0}
              role="button"
              aria-label={isFocus ? `${n.name} (focused)` : `Focus tree on ${n.name}`}
            >
              <circle cx={pos.x} cy={pos.y} r={isFocus ? 34 : 26} />
              {n.portrait_filename && (
                <image
                  href={`/assets/characters/${n.portrait_filename}`}
                  x={pos.x - (isFocus ? 34 : 26)}
                  y={pos.y - (isFocus ? 34 : 26)}
                  width={(isFocus ? 34 : 26) * 2}
                  height={(isFocus ? 34 : 26) * 2}
                  clipPath={`url(#clip-${n.id})`}
                  preserveAspectRatio="xMidYMin slice"
                  onError={(e) => { e.currentTarget.style.display = "none"; }}
                />
              )}
              <text x={pos.x} y={pos.y + (isFocus ? 52 : 44)}>
                {n.name}
              </text>
            </motion.g>
          );
        })}
      </svg>
      <div className="tree-hint">
        {focusNode ? `Centered on ${focusNode.name}. ` : ""}click any node to re-center
      </div>
    </div>
  );
}