import re

from openai import max_retries
from ..scripts.DEFAULT import *

global __embed_model_cache__
__embed_model_cache__ = {}

def get_embedding(model_name: str = "alibaba-nlp/gte-multilingual-base", show_progress: bool = True):
    """get the embedding model."""
    from langchain_huggingface import HuggingFaceEmbeddings
    import torch

    if model_name in __embed_model_cache__:
        return __embed_model_cache__[model_name]
    embeddings = HuggingFaceEmbeddings(
                model_name=model_name,
                show_progress=show_progress,
                model_kwargs={'device': 'cuda' if torch.cuda.is_available() else 'cpu', 'trust_remote_code':True},
                encode_kwargs={'batch_size': 15}
            )
    __embed_model_cache__[model_name] = embeddings
    return embeddings

def get_llm(model_key: str = "gpt-oss 20B", max_tokens: int = 2048, temperature: float = 0.1):
    """get the chat model."""
    from langchain.chat_models import init_chat_model

    provider = AVAILABLE_MODELS[model_key][1]
    if provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model = AVAILABLE_MODELS[model_key][0],
            reasoning = False
        )
    elif provider == "hf":
        from langchain_huggingface import ChatHuggingFace
        return ChatHuggingFace(
            model = AVAILABLE_MODELS[model_key][0],
            reasoning = False
        )

    return init_chat_model(
        model=f"{AVAILABLE_MODELS[model_key][1]}:{AVAILABLE_MODELS[model_key][0]}",
        max_retries = 3
    )

def clear_cache():
    """clear the cache."""
    global __db_cache__, __embed_model_cache__
    __db_cache__ = None
    __embed_model_cache__ = {}

