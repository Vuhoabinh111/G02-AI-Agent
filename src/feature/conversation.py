from ollama import chat
from platformdirs import user_data_dir
from ..scripts.agent import chatbot_logic
from typing import List, Generator
from ..scripts.DEFAULT import PERSONA, MAX_HISTORY_CONVERSATION, USER_DATA_RAW
from ..utils import log

import random, os
global thread_id, interupt
thread_id = random.randint(100000, 999999)
interupt = False

global history
history = []

def respond(message: str, chat_history: List[List[str]], selected_model_key: str, customer_data:str) -> Generator[List[List[str]], None, None]:
    """Wrapper function to connect chatbot_logic with Gradio's state."""
    # Append the user's message and a blank space for the bot's response.
    global history
    if len(chat_history) < 1 or chat_history[-1] == [None, None]:
        history = [["", ""]]
    else:
        history.append(chat_history[-1])

    chat_history.append([message, ""])
    
    conversation = "\n".join([f"User:{item[0]}\nBot:{item[1]}\n" for item in history[-MAX_HISTORY_CONVERSATION:]])
    conversation += f"User:{message}\nBot:"
    
    additional_info = ""

    if customer_data:
        additional_info += f"CUSTOMER: {customer_data}"
    
    prompt = PERSONA.format(additional_info=additional_info, conversation=conversation)

    # Iterate over the generator from chatbot_logic and update the history.
    for token in chatbot_logic(message=prompt, selected_model_key=selected_model_key):
        # Update the last message in chat_history with the new token.
        chat_history[-1][1] += token
        yield chat_history
    log(f"PROMPT:{prompt}")
    log(chat_history[-1])

def start_new_chat(chat_history: List[List[str]]):
    """Resets the chat history and the message input."""
    import gradio as gr
    chat_history = [[None, None]]
    global thread_id
    thread_id = random.randint(100000, 999999)
    return (
        chat_history,
        gr.update(value="", placeholder="What can I help you with?"),
    )

def interupt_conversation():
    global interupt
    interupt = True