import gradio as gr
from api.phone_call import initiate_call
from api.deepgram_transcription import start_deepgram_transcription
from api.text_to_speech import convert_text_to_speech
from api.ai_model import get_ai_response

def create_interface() -> gr.Blocks:
    with gr.Blocks() as interface:
        gr.Markdown("## Prank Call AI Service")
        
        with gr.Tab("Initiate Call"):
            phone_number_input = gr.Textbox(label="Enter Phone Number")
            call_button = gr.Button("Initiate Call")
            call_output = gr.Textbox(label="Call Status")
            call_button.click(fn=initiate_call, inputs=phone_number_input, outputs=call_output)

        with gr.Tab("Transcription"):
            audio_url_input = gr.Textbox(label="Enter Audio URL")
            transcribe_button = gr.Button("Start Transcription")
            transcription_output = gr.Textbox(label="Transcription Status")
            transcribe_button.click(fn=start_deepgram_transcription, inputs=audio_url_input, outputs=transcription_output)

        with gr.Tab("Text to Speech"):
            text_input = gr.Textbox(label="Enter Text")
            tts_button = gr.Button("Convert to Speech")
            tts_output = gr.Textbox(label="TTS Status")
            tts_button.click(fn=convert_text_to_speech, inputs=text_input, outputs=tts_output)

        with gr.Tab("AI Response"):
            ai_text_input = gr.Textbox(label="Enter Text for AI Response")
            ai_button = gr.Button("Get AI Response")
            ai_output = gr.Textbox(label="AI Response")
            ai_button.click(fn=get_ai_response, inputs=ai_text_input, outputs=ai_output)

    return interface

if __name__ == "__main__":
    interface = create_interface()
    interface.launch()