"""
Tests for the Lore Analyst. Deliberately does NOT test real Gemini calls or
real embedding generation — those need network access this test environment
may not have, and shouldn't be part of a unit test suite anyway. What's
tested here is everything within our control: that the corpus builder pulls
correct, clean data, and that the query endpoint fails gracefully without an
API key rather than crashing.
"""
import pytest
from mongomock_motor import AsyncMongoMockClient
from app.rag.corpus_builder import build_corpus, _plain
from app.repositories.character_repository import CharacterRepository
from app.repositories.power_repository import PowerRepository
from app.repositories.relationship_repository import RelationshipRepository
from app.repositories.arc_repository import ArcRepository


def test_plain_handles_both_enum_and_string():
    assert _plain("shikai") == "shikai"

    class FakeEnum:
        value = "bankai"
    assert _plain(FakeEnum()) == "bankai"


@pytest.mark.asyncio
async def test_build_corpus_produces_clean_chunks():
    mock_db = AsyncMongoMockClient()["lore_analyst_corpus_test"]
    char_repo = CharacterRepository(mock_db)
    power_repo = PowerRepository(mock_db)
    rel_repo = RelationshipRepository(mock_db)
    arc_repo = ArcRepository(mock_db)

    char_doc = await char_repo.create({
        "name": "Ichigo Kurosaki", "biography": "Test bio.",
        "personality": None, "appearance": None, "arc_ids": [], "source_ids": [], "clan_id": None,
        "portrait_filename": None, "full_body_filename": None,
    })
    char_id = char_doc["_id"]
    await power_repo.create({
        "character_id": char_id, "power_type": "bankai", "ability_description": "Test power.",
        "other_type_label": None, "rules_and_limitations": None, "evolution_notes": None,
        "first_shown_source_id": None,
    })
    await arc_repo.create({"name": "Test Arc", "order_index": 1, "chapter_range": None, "episode_range": None})

    ids, documents, metadatas = await build_corpus(char_repo, power_repo, rel_repo, arc_repo)

    assert len(ids) == 3  # 1 character + 1 power + 1 arc, 0 relationships
    joined = " ".join(documents)
    assert "PowerType" not in joined  # no leaked enum repr
    assert "bankai" in joined
    assert "Ichigo Kurosaki" in joined


def test_query_without_api_key_returns_503(test_client):
    resp = test_client.post(
        "/lore-analyst/query",
        json={"question": "test question", "spoiler_boundary": "Episode 1"},
    )
    assert resp.status_code == 503
    assert "GEMINI_API_KEY" in resp.json()["detail"]


def test_query_rejects_empty_question(test_client):
    resp = test_client.post(
        "/lore-analyst/query",
        json={"question": "", "spoiler_boundary": "Episode 1"},
    )
    assert resp.status_code == 422