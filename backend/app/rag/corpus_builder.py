"""
Builds the RAG corpus from the same repositories the rest of the app already
uses — never touches MongoDB directly, never duplicates query logic. Every
chunk carries metadata identifying exactly what it came from, so the Lore
Analyst can always cite its source rather than answer from an untraceable blob.
"""


def _plain(value):
    """Normalizes an Enum-or-string field to its plain string value."""
    return getattr(value, "value", value)


async def build_corpus(character_repo, power_repo, relationship_repo, arc_repo):
    """Returns (ids, documents, metadatas) ready to upsert into the vector store."""
    ids, documents, metadatas = [], [], []

    characters = await character_repo.list_all()
    char_by_id = {c["_id"]: c for c in characters}

    for c in characters:
        parts = [f"{c['name']}. {c.get('biography', '')}"]
        if c.get("personality"):
            parts.append(f"Personality: {c['personality']}")
        if c.get("appearance"):
            parts.append(f"Appearance: {c['appearance']}")
        ids.append(f"character:{c['_id']}")
        documents.append(" ".join(parts))
        metadatas.append({"type": "character", "name": c["name"], "character_id": c["_id"]})

    powers = await power_repo.list_all()
    for p in powers:
        owner = char_by_id.get(p["character_id"])
        owner_name = owner["name"] if owner else "Unknown character"
        label = p.get("other_type_label") or _plain(p["power_type"])
        text = f"{owner_name}'s {label}: {p['ability_description']}"
        if p.get("rules_and_limitations"):
            text += f" Rules and limitations: {p['rules_and_limitations']}"
        if p.get("evolution_notes"):
            text += f" Later evolution: {p['evolution_notes']}"
        ids.append(f"power:{p['_id']}")
        documents.append(text)
        metadatas.append({"type": "power", "name": f"{owner_name}'s {label}", "character_id": p["character_id"]})

    relationships = await relationship_repo.list_all()
    for r in relationships:
        a = char_by_id.get(r["character_a_id"])
        b = char_by_id.get(r["character_b_id"])
        a_name = a["name"] if a else "Unknown"
        b_name = b["name"] if b else "Unknown"
        text = f"Relationship between {a_name} and {b_name}: {_plain(r['relationship_type'])}."
        if r.get("plot_relevance_note"):
            text += f" {r['plot_relevance_note']}"
        ids.append(f"relationship:{r['_id']}")
        documents.append(text)
        metadatas.append({"type": "relationship", "name": f"{a_name} & {b_name}"})

    arcs = await arc_repo.list_all()
    for a in arcs:
        text = f"Story arc: {a['name']}."
        if a.get("chapter_range"):
            text += f" Chapters: {a['chapter_range']}."
        if a.get("episode_range"):
            text += f" Episodes: {a['episode_range']}."
        ids.append(f"arc:{a['_id']}")
        documents.append(text)
        metadatas.append({"type": "arc", "name": a["name"]})

    return ids, documents, metadatas