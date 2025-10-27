# Local retriever tool
from langchain.tools.retriever import create_retriever_tool
from ..utils.database import get_db

global user_knowledge_retriever
user_knowledge_retriever = create_retriever_tool(
    get_db().as_retriever(),
    name="user_document_retriever",
    description="tài liệu đã được upload bởi người dùng"
)

def read_file(file_name:str) -> str:
    """
    Lấy nội dung file từ file_name.
    Ví dụ: "ABC.pdf"
    """
    from ..scripts.DEFAULT import USER_DATA_DIGESTABLE
    prefix = file_name.split(".")[0]
    with open(f"{USER_DATA_DIGESTABLE}/{prefix}.txt", "r", encoding="utf-8") as f:
        return f.read()