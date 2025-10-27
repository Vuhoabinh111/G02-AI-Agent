from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent


from ..utils.models import get_llm
# from .docs_retrieve import user_knowledge_retriever
from ..utils import log

from ..scripts.DEFAULT import JUDGE_POST_PROMPT

@tool
def judge_post_agent(customer_data:str, post: str):
    """
    Sử dụng một agent nhỏ hơn để thẩm định và đánh giá các bài viết trực tuyến để bảo vệ danh dự, uy tín và an toàn cho khách hàng.
    """
    # llm = get_llm("llama3.1 8B")
    # agent_executor = create_react_agent(model=llm, tools=[retriever])

    # from langchain.schema import AIMessage

    # yield "="*20

    # try:
    #     for chunk in agent_executor.stream(
    #         {"messages": [{"role": "user", "content": JUDGE_POST_PROMPT.format(customer = customer_data, post = post)}]},
    #         stream_mode="values",
    #     ):
    #         print(f"###{chunk}")
    #         yield chunk["messages"][-1]

    # except Exception as e:
    #     yield f"An error occurred: {e}"
    # yield "="*20

@tool
def legal_analyze_prompt(customer_data:str, post: str) -> str:
    """
    Dùng để tạo 1 prompt hoàn chỉnh phục vụ việc đánh giá và phân tích bài đăng.
    """
    return JUDGE_POST_PROMPT.format(customer=customer_data, post=post)