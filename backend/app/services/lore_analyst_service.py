"""
The actual AI Lore Analyst. Retrieves grounded context from the vector store,
then asks Gemini Flash to answer USING ONLY that context — never from its own
general knowledge of Bleach, which the design doc explicitly forbids (it could
hallucinate details not actually in this project's structured data, or leak
spoilers past what the person has said they've reached).
"""

from google import genai
from app.core.config import settings
from app.rag import vector_store

SYSTEM_INSTRUCTIONS = """You are the Lore Analyst for Bleach Codex, an AI-augmented Bleach encyclopedia.

RULES, IN ORDER OF IMPORTANCE:
0. SCOPE: you only discuss Bleach — its characters, story, powers, world, and this Codex project \
itself. If the question is unrelated to Bleach (general trivia, coding help, other franchises, \
anything off-topic), decline briefly and say you're scoped to Bleach lore only. Do not answer the \
off-topic question even partially.
1. SPOILER BOUNDARY (never break this, regardless of source): the person has said they've reached \
"{boundary}". If any part of your answer would reveal, hint at, or confirm/deny something that \
happens after that point in the story, refuse that part specifically and say it's beyond their \
current point — even if it's sitting right there in the retrieved context, and even if you're \
confident about it from general knowledge. Partial answers are fine: answer what's safe, withhold \
what isn't.
2. GROUNDING PREFERENCE: if the CONTEXT below actually contains what's needed to answer, use it and \
cite it — this project's own structured data takes priority over your general knowledge, since it's \
been specifically researched and verified for this encyclopedia.
3. GENERAL-KNOWLEDGE FALLBACK: if the CONTEXT doesn't cover the question, you may answer from your \
own general knowledge of the Bleach manga/anime instead of refusing — but you MUST say plainly that \
this part isn't yet in the Codex's own database, so the person always knows which kind of answer \
they're getting. Never blend the two without distinguishing them.
4. Keep answers conversational and concise — a few sentences, not an essay, unless genuinely asked \
for depth.
"""


def _build_context_block(chunks: list[dict]) -> str:
    if not chunks:
        return "(no relevant context found)"
    lines = []
    for c in chunks:
        lines.append(f"- [{c['metadata']['type']}: {c['metadata']['name']}] {c['text']}")
    return "\n".join(lines)


def answer_question(question: str, spoiler_boundary: str) -> dict:
    """
    Returns {"answer": str, "sources": [{"type": str, "name": str}, ...]}.
    Raises RuntimeError if no Gemini API key is configured — caller decides
    how to surface that rather than silently returning a fake answer.
    """
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add it to backend/.env to enable the Lore Analyst."
        )

    chunks = vector_store.query(question, n_results=6)
    context_block = _build_context_block(chunks)

    prompt = (
        f"{SYSTEM_INSTRUCTIONS.format(boundary=spoiler_boundary)}\n\n"
        f"CONTEXT:\n{context_block}\n\n"
        f"QUESTION: {question}"
    )

    client = genai.Client(api_key=settings.gemini_api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    seen = set()
    sources = []
    for c in chunks:
        key = (c["metadata"]["type"], c["metadata"]["name"])
        if key not in seen:
            seen.add(key)
            sources.append({"type": c["metadata"]["type"], "name": c["metadata"]["name"]})

    return {"answer": response.text, "sources": sources}