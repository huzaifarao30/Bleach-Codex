import { useState } from "react";
import { BrowserRouter, Routes, Route, NavLink, useLocation } from "react-router-dom";
import AmbientBackground from "./animations/AmbientBackground";
import Landing from "./pages/Landing";
import Characters from "./pages/Characters";
import CharacterDetail from "./pages/CharacterDetail";
import FamilyTree from "./pages/FamilyTree";
import Powers from "./pages/Powers";
import Foreshadowing from "./pages/Foreshadowing";
import LoreAnalyst from "./pages/LoreAnalyst";

function Nav() {
  const [open, setOpen] = useState(false);
  const location = useLocation();

  // Close the menu automatically whenever the route changes.
  useState(() => {
    setOpen(false);
  }, [location.pathname]);

  return (
    <nav className="nav">
      <NavLink to="/" className="nav-brand" onClick={() => setOpen(false)}>
        BLEACH<span>CODEX</span>
      </NavLink>

      <button
        className="nav-toggle"
        aria-label={open ? "Close menu" : "Open menu"}
        aria-expanded={open}
        onClick={() => setOpen((o) => !o)}
      >
        <span />
        <span />
        <span />
      </button>

      <div className={`nav-links${open ? " open" : ""}`}>
        <NavLink to="/characters" onClick={() => setOpen(false)}>Characters</NavLink>
        <NavLink to="/powers" onClick={() => setOpen(false)}>Powers</NavLink>
        <NavLink to="/foreshadowing" onClick={() => setOpen(false)}>Foreshadowing</NavLink>
        <NavLink to="/lore-analyst" onClick={() => setOpen(false)}>Lore Analyst</NavLink>
      </div>
    </nav>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <AmbientBackground />
        <Nav />
        <main className="app-content">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/characters" element={<Characters />} />
            <Route path="/characters/:id" element={<CharacterDetail />} />
            <Route path="/family-tree" element={<FamilyTree />} />
            <Route path="/family-tree/:id" element={<FamilyTree />} />
            <Route path="/powers" element={<Powers />} />
            <Route path="/foreshadowing" element={<Foreshadowing />} />
            <Route path="/lore-analyst" element={<LoreAnalyst />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}