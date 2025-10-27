import gradio as gr
import json
import os

os.environ['OLLAMA_GPU_LAYERS'] = '-1'
os.environ['OLLAMA_NUM_PARALLEL'] = '1'
os.environ['OLLAMA_MAX_LOADED_MODELS'] = '1'

os.environ['MISTRAL_API_KEY'] = 'hjmdJZpVMk3GLpiRWSQMkmE2pHmeBecA'

from src.style.theme import adjust_theme
from src.scripts.DEFAULT import *
from src.feature import respond, upload_file, start_new_chat, interupt_conversation

with open("./src/style/style.css", 'r', encoding='utf-8') as f:
    css = f.read()

set_theme = adjust_theme()
customer_data = json.loads(CUSTOMER)

def show_edit_form(current_data):
    """Populates the form with current data and makes it visible."""
    return {
        edit_form: gr.update(open=True),
        customer_name_input: current_data['name'],
        customer_birth_input: current_data['birth'],
        customer_pos_input: current_data['current_position'],
        customer_email_input: current_data['email'],
    }

def save_customer_info(current_data, name, birth, position, email):
    """Updates the customer data state and hides the form."""
    current_data['name'] = name
    current_data['birth'] = int(birth)
    current_data['current_position'] = position
    current_data['email'] = email
    
    gr.Info("Customer information saved successfully!")
    
    # Return the updated data to the state and close the accordion
    return {
        customer_state: current_data,
        edit_form: gr.update(open=False)
    }

def show_file_upload_form():
    """Shows the file upload form."""
    return {
        file_upload_form: gr.update(open=True)
    }


with gr.Blocks(title="AI Guardian", theme=set_theme, css=css) as demo:
    # Header
    gr.Markdown(
        '''
        # <center>AI Guardian<center>
        <center>Your Guardian AI Assistant.<center>
        '''
    )

    # State to hold customer data
    customer_state = gr.State(customer_data)

    # Main Interface
    with gr.Row(elem_classes="col-container"):

        # 1st Column: Control Panel
        with gr.Column():
            model_selector = gr.Dropdown(
                label="Select Model",
                choices=list(AVAILABLE_MODELS.keys()),
                value=DEFAULT_MODEL_KEY,
            )
            
            new_chat_btn = gr.Button(
                "New Chat",
                variant="secondary",
                elem_id="btn_transparent",
            )

            add_file_btn = gr.Button(
                "Add File", 
                variant="secondary"
            )
            with gr.Accordion("File Upload", open=False) as file_upload_form:
                file_input = gr.File(label="Upload File", file_types=[".pdf", ".txt", ".xlsx"])
                upload_file_btn = gr.Button("Upload", variant="primary")
            gr.Markdown(
                "--- \n"
                "**Note:** Only support PDF, XLSX and TXT"
            )

        # 2nd Column: Chat Interface
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(
                label="Chat Window", 
                height=600,
                type="tuples"
            )
            
            msg_input = gr.Textbox(
                label="Your Message", 
                placeholder="What can I help you with?",
            )
            gr.update(value="", placeholder="What can I help you with?")

        # 3rd Column: User Info
        with gr.Column():

            edit_info_btn = gr.Button("Edit Customer Info", variant="secondary")

            with gr.Accordion("Customer Details", open=True) as edit_form:
                customer_name_input = gr.Textbox(label="Name")
                customer_birth_input = gr.Number(label="Birth/Establish Year", precision=0)
                customer_pos_input = gr.Textbox(label="Description", lines=3)
                customer_email_input = gr.Textbox(label="Email")
                save_info_btn = gr.Button("Save Changes", variant="primary")
            # --- End of Feature ---
            
            gr.Markdown(
                "--- \n"
                "**Note:** Your conversations are saved for quality assurance."
            )

    # --- Event Listeners ---
    msg_input.submit(
        respond,
        [msg_input, chatbot, model_selector, customer_state],
        [chatbot]
    ).then(
        lambda: gr.update(value=""), None, [msg_input], queue=False
    )

    upload_file_btn.click(
        fn=upload_file,
        inputs=file_input,
        outputs = [file_upload_form],
        queue=False
    )

    new_chat_btn.click(
        start_new_chat,
        inputs=[chatbot],
        outputs=[chatbot, msg_input],
        queue=False
    )

    edit_info_btn.click(
        fn=show_edit_form,
        inputs=[customer_state],
        outputs=[
            edit_form,
            customer_name_input, 
            customer_birth_input, 
            customer_pos_input, 
            customer_email_input
        ],
        queue=False
    )
    
    save_info_btn.click(
        fn=save_customer_info,
        inputs=[
            customer_state,
            customer_name_input,
            customer_birth_input,
            customer_pos_input,
            customer_email_input
        ],
        outputs=[customer_state, edit_form],
        queue=False
    )

    add_file_btn.click(
        fn=show_file_upload_form,
        inputs=None,
        outputs=[file_upload_form],
        queue=False
    )

# --- Launch the App ---
if __name__ == "__main__":
    demo.launch(debug=True, share=True, inbrowser=False, show_api=False)