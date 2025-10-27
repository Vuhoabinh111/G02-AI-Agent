# from .web_search import web_search
from .check_date import check_date
from .docs_retrieve import user_knowledge_retriever, read_file
from .judge_llm import judge_post_agent, legal_analyze_prompt
from .check_user_file import list_uploaded_files

tools = [
    # web_search,
    check_date,
    user_knowledge_retriever,
    read_file,
    list_uploaded_files,
    # legal_analyze_prompt,
    # judge_post_agent,
]

__all__ = [
    "tools", # Chỉ import được biến `tools` khi gọi đến folder này
]