import asyncio
import sys

# Windows' default ProactorEventLoop has known issues with async TLS/SSL
# handshakes, which can cause async MongoDB (Atlas) connections to hang
# indefinitely even though sync connections and plain TCP work fine.
# This forces the alternate, more compatible event loop policy on Windows only.
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import characters, relationships, family_tree, powers, arcs, sources, lore_events, lore_analyst

app = FastAPI(
    title="Bleach Codex API",
    description="AI-augmented lore encyclopedia backend.",
    version="0.1.0",
)

# Allow the local React dev server to call this API from the browser.
# Tighten allow_origins to the real deployed frontend URL in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(characters.router)
app.include_router(relationships.router)
app.include_router(family_tree.router)
app.include_router(powers.router)
app.include_router(arcs.router)
app.include_router(sources.router)
app.include_router(lore_events.router)
app.include_router(lore_analyst.router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}