from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)
from app.rag.embedder import embed_text, get_embed_model
from app.core.config import settings
import uuid

COLLECTION_NAME = "adaptiq_documents"
VECTOR_SIZE = 384

_client = None


def get_qdrant_client():
    global _client
    if _client is None:
        _client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )
        ensure_collection()
    return _client


def ensure_collection():
    client = QdrantClient(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT
    )

    existing = [c.name for c in client.get_collections().collections]

    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )
        print(f"[Qdrant] Created collection: {COLLECTION_NAME}")
    else:
        print(f"[Qdrant] Collection already exists: {COLLECTION_NAME}")


def store_nodes(nodes: list, user_id: str, filename: str):
    client = get_qdrant_client()

    # Ensure embedding model is loaded
    get_embed_model()

    points = []

    for node in nodes:
        vector = embed_text(node.text)

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "text": node.text,
                "source": filename,
                "user_id": user_id,
                "metadata": node.metadata
            }
        )

        points.append(point)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"[Qdrant] Stored {len(points)} vectors for user {user_id}")
    return len(points)


def retrieve_relevant_chunks(query: str, user_id: str, top_k: int = 5) -> list:
    client = get_qdrant_client()

    query_vector = embed_text(query)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=user_id)
                )
            ]
        ),
        limit=top_k,
        with_payload=True
    )

    chunks = []

    for result in results.points:
        chunks.append({
            "text": result.payload.get("text", ""),
            "source": result.payload.get("source", ""),
            "score": result.score
        })

    print(
        f"[Qdrant] Retrieved {len(chunks)} chunks for query: {query[:50]}..."
    )

    return chunks


def delete_user_documents(user_id: str, filename: str = None):
    client = get_qdrant_client()

    must_conditions = [
        FieldCondition(
            key="user_id",
            match=MatchValue(value=user_id)
        )
    ]

    if filename:
        must_conditions.append(
            FieldCondition(
                key="source",
                match=MatchValue(value=filename)
            )
        )

    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=Filter(
            must=must_conditions
        )
    )

    print(f"[Qdrant] Deleted documents for user {user_id}")