from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

_embed_model = None

def get_embed_model():
    global _embed_model
    if _embed_model is None:
        print("[Embedder] Loading embedding model (first time takes ~30 seconds)...")
        _embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )
        Settings.embed_model = _embed_model
        print("[Embedder] Embedding model loaded!")
    return _embed_model

def embed_text(text: str) -> list:
    model = get_embed_model()
    embedding = model.get_text_embedding(text)
    return embedding