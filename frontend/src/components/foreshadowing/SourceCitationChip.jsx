/**
 * Always-visible inline citation. Per the PRD, grounding must render by
 * default — never hidden behind a hover-only tooltip.
 */
export default function SourceCitationChip({ source }) {
  return (
    <span className="source-chip" title={source.note || undefined}>
      {source.reference}
    </span>
  );
}