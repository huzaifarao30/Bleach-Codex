// All backend communication goes through this file — components never fetch directly.
// Set VITE_API_URL in a .env file to point elsewhere; defaults to the local FastAPI server.

const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

async function get(path) {
  const resp = await fetch(`${BASE_URL}${path}`);
  if (!resp.ok) {
    throw new Error(`API ${resp.status}: ${path}`);
  }
  return resp.json();
}

export const api = {
  listCharacters: () => get("/characters/"),
  getCharacterFull: (id) => get(`/characters/${id}/full`),
  getFamilyTree: (id, depth = 2) => get(`/family-tree/${id}?depth=${depth}`),
  listPowers: () => get("/powers/"),
  listArcs: () => get("/arcs/"),
  listLoreEvents: (status) =>
    get(status ? `/lore-events/?status=${status}` : "/lore-events/"),
  askLoreAnalyst: async (question, spoilerBoundary) => {
    const resp = await fetch(`${BASE_URL}/lore-analyst/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, spoiler_boundary: spoilerBoundary }),
    });
    const body = await resp.json().catch(() => ({}));
    if (!resp.ok) {
      const err = new Error(body.detail || `API ${resp.status}`);
      err.status = resp.status;
      throw err;
    }
    return body;
  },
};