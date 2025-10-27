from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from typing import Generator

from ..utils.models import get_llm
from ..tools import tools
from ..utils import log

global __agent_cache__
# memory = MemorySaver()
# Save the system prompt into memory

def chatbot_logic(
    message: str,
    selected_model_key: str,
) -> Generator[str, None, None]:
    """
    Core function that uses a LangChain ReAct agent to respond to a user message.
    It returns a generator to enable streaming.
    """
    from ..feature.conversation import thread_id, interupt
    # print(thread_id)
    from langchain.schema import AIMessage

    log(selected_model_key)
    # Create the LLM with streaming enabled.
    llm = get_llm(selected_model_key)
    # config = {"configurable": {"thread_id": str(thread_id)}}
    agent_executor = create_react_agent(model=llm, tools=tools)

    try:
        for chunk in agent_executor.stream(
            {"messages": [{"role": "user", "content": message}]},
            # config=config,
            stream_mode="messages",
        ):
            if interupt:
                interupt = False
                break
            # print(chunk)
            if chunk[0].additional_kwargs == {} and isinstance(chunk[0], AIMessage):
                yield str(chunk[0].content)
            else:
                yield f"**Tool calling...**\n{str(chunk[0].name)}\n\n"

    except Exception as e:
        yield f"An error occurred: {e}"