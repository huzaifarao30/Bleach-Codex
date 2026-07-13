import { useEffect, useRef } from "react";
import { useReducedMotion } from "framer-motion";

/**
 * Very low-intensity ambient particle drift behind the whole app.
 * Fully disabled (renders nothing) when prefers-reduced-motion is set,
 * per the PRD's non-negotiable motion rule.
 */
export default function AmbientBackground() {
  const canvasRef = useRef(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    let raf;

    const particles = Array.from({ length: 52 }, () => {
      const roll = Math.random();
      return {
        x: Math.random(),
        y: Math.random(),
        r: 0.6 + Math.random() * 1.4,
        vy: 0.00012 + Math.random() * 0.0003,
        kind: roll > 0.88 ? "blood" : roll > 0.68 ? "gold" : "soul",
      };
    });

    function resize() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener("resize", resize);

    function frame() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (const p of particles) {
        p.y -= p.vy;
        if (p.y < -0.02) p.y = 1.02;
        ctx.beginPath();
        ctx.arc(p.x * canvas.width, p.y * canvas.height, p.r, 0, Math.PI * 2);
        ctx.fillStyle =
          p.kind === "blood"
            ? "rgba(224, 41, 63, 0.22)"
            : p.kind === "gold"
            ? "rgba(212, 175, 47, 0.20)"
            : "rgba(159, 184, 204, 0.10)";
        ctx.fill();
      }
      raf = requestAnimationFrame(frame);
    }
    frame();

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", resize);
    };
  }, [reduce]);

  if (reduce) return null;

  return (
    <canvas
      ref={canvasRef}
      aria-hidden="true"
      style={{ position: "fixed", inset: 0, zIndex: 0, pointerEvents: "none" }}
    />
  );
}