import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import AmbientBackground from "./animations/AmbientBackground";
import Landing from "./pages/Landing";
import Characters from "./pages/Characters";
import CharacterDetail from "./pages/CharacterDetail";
import FamilyTree from "./pages/FamilyTree";
import Powers from "./pages/Powers";
import Foreshadowing from "./pages/Foreshadowing";
import LoreAnalyst from "./pages/LoreAnalyst";

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <AmbientBackground />
        <nav className="nav">
          <NavLink to="/" className="nav-brand">
            BLEACH<span>CODEX</span>
          </NavLink>
          <div className="nav-links">
            <NavLink to="/characters">Characters</NavLink>
            <NavLink to="/powers">Powers</NavLink>
            <NavLink to="/foreshadowing">Foreshadowing</NavLink>
            <NavLink to="/lore-analyst">Lore Analyst</NavLink>
          </div>
        </nav>
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