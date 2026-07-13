from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from app.core.database import get_database
from app.repositories.character_repository import CharacterRepository
from app.repositories.power_repository import PowerRepository
from app.repositories.relationship_repository import RelationshipRepository
from app.repositories.arc_repository import ArcRepository
from app.rag import corpus_builder, vector_store
from app.services import lore_analyst_service

router = APIRouter(prefix="/lore-analyst", tags=["Lore Analyst"])


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1)
    spoiler_boundary: str = Field(..., min_length=1, description="How far the person has watched/read.")


class QueryResponse(BaseModel):
    answer: str
    sources: list[dict]


@router.post("/query", response_model=QueryResponse)
async def query_lore_analyst(payload: QueryRequest):
    try:
        result = lore_analyst_service.answer_question(payload.question, payload.spoiler_boundary)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    return result


@router.post("/reindex")
async def reindex(db=Depends(get_database)):
    """
    Rebuilds the vector store from whatever's currently in the database.
    Run this after re-seeding, or after adding/editing any character, power,
    relationship, or arc — the Lore Analyst only knows what's been indexed,
    not the live database, until this runs.
    """
    character_repo = CharacterRepository(db)
    power_repo = PowerRepository(db)
    relationship_repo = RelationshipRepository(db)
    arc_repo = ArcRepository(db)

    vector_store.reset_collection()
    ids, documents, metadatas = await corpus_builder.build_corpus(
        character_repo, power_repo, relationship_repo, arc_repo
    )
    vector_store.upsert(ids, documents, metadatas)
    return {"indexed_chunks": len(ids)}