# Local DB
# This module provides functions to initialize, add to, and retrieve from a local vector database.
from ..scripts.DEFAULT import *
from ..utils.models import get_embedding
from .markdown_splitter import split_document

global __db_cache__
__db_cache__ = None

def init_db(directory_path: str = VECTORSTORE_PATH, chunk_size:int = CHUNK_SIZE, chunk_overlap:int = CHUNK_OVERLAP):
    """initialize the local database."""
    from langchain_community.document_loaders import DirectoryLoader
    from langchain_community.vectorstores import FAISS

    # reset_db()
    loader = DirectoryLoader(directory_path, show_progress=True)
    docs = split_document(loader.load(), chunk_size, chunk_overlap)
    embeddings = get_embedding(EMBEDDING_MODEL_ID, show_progress=True)
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(VECTORSTORE_PATH)
    # Update cache
    update_db(db)
    return db

def add_file(file_path: str, chunk_size:int = CHUNK_SIZE, chunk_overlap:int = CHUNK_OVERLAP):
    """add a file to the local database."""
    from langchain_community.document_loaders import TextLoader

    loader = TextLoader(file_path, encoding="utf-8")
    docs = split_document(loader.load(), chunk_size, chunk_overlap)
    db = get_db()
    db.add_documents(docs)
    db.save_local(VECTORSTORE_PATH)
    print("Saved")
    # Update cache
    update_db(db)
    return db

def remove_file(file_path: str):
    """remove a file from the local database."""
    import os

    if not os.path.exists(file_path):
        raise ValueError(f"File {file_path} does not exist.")
    db = get_db()
    # Assuming the file name is unique in the database
    file_name = os.path.basename(file_path)
    ids_to_remove = [doc_id for doc_id, metadata in db.index_to_docstore_id.items() if metadata.get('source', '') == file_name]
    if not ids_to_remove:
        raise ValueError(f"File {file_path} not found in the database.")
    db.delete(ids=ids_to_remove)
    db.save_local(VECTORSTORE_PATH)
    # Update cache
    update_db(db)
    return db

def reset_db(vectorstore_path: str = VECTORSTORE_PATH):
    """reset the local database."""
    import shutil, os

    global __db_cache__
    __db_cache__ = None
    if os.path.exists(vectorstore_path):
        shutil.rmtree(vectorstore_path)
    init_db()

def get_db(vectorstore_path: str = VECTORSTORE_PATH, user_data_digestable: str = USER_DATA_DIGESTABLE):
    """get the local database."""
    from langchain_community.vectorstores import FAISS
    global __db_cache__
    if __db_cache__ is None:
        try:
            __db_cache__ = FAISS.load_local(vectorstore_path, get_embedding(EMBEDDING_MODEL_ID, show_progress=False), allow_dangerous_deserialization=True)
        except:
            print(f"{vectorstore_path} not found, creating new database...{user_data_digestable}")
            init_db(user_data_digestable)
    return __db_cache__

def update_db(db):
    global __db_cache__
    __db_cache__ = db

    from langchain.tools.retriever import create_retriever_tool

    global retriever
    retriever = create_retriever_tool(
        get_db().as_retriever(),
        name="user_document_retriever",
        description="tài liệu đã được upload bởi người dùng."
    )