const FAMILY = new Set(["parent", "child", "sibling", "spouse"]);
const CONFLICT = new Set(["rival", "enemy"]);
// everything else (mentor/student, captain/lieutenant, ally, friend, etc.) = bond/gold

/**
 * Displays a relationship type EXACTLY as returned by the API.
 * Direction is already resolved server-side (PRD Section 5.1) —
 * this component must never re-interpret it.
 */
export default function RelationshipBadge({ type }) {
  const category = FAMILY.has(type) ? "family" : CONFLICT.has(type) ? "conflict" : "bond";
  return <span className={`rel-badge ${category}`}>{type}</span>;
}