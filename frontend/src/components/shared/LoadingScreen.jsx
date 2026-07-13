import { useReducedMotion } from "framer-motion";

/**
 * Branded loading indicator: four threads weave around a pulsing gold
 * node. Adapted from a Tailwind/shadcn reference design into plain CSS
 * using this project's own color tokens — no framework migration needed
 * for one spinner.
 */
export default function LoadingScreen({ label = "Loading…" }) {
  const reduce = useReducedMotion();

  return (
    <div className="loading-screen">
      <div className={`weave-spinner${reduce ? " reduced" : ""}`}>
        <div className="weave-thread t1" />
        <div className="weave-thread t2" />
        <div className="weave-thread t3" />
        <div className="weave-thread t4" />
        <div className="weave-node" />
      </div>
      <div className="loading-label">{label}</div>
    </div>
  );
}