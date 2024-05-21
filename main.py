import gradio as gr
from deepgram_transcription import start_deepgram_transcription
from text_to_speech import convert_text_to_speech
from ai_model import get_ai_response
from phone_call import initiate_call

def start_transcription(audio_url):
    start_deepgram_transcription(audio_url)
    return "Transcription started"

def text_to_speech_conversion(text):
    result = convert_text_to_speech(text)
    return result

def ai_response(text):
    messages = [
        {"role": "system", "content": "You are an AI designed to engage in prank calls."},
        {"role": "user", "content": text},
    ]
    response = get_ai_response(messages)
    return response

def make_call(phone_number):
    message_url = "http://your-server-url/message"  # Placeholder URL for Twilio to fetch instructions
    result = initiate_call(phone_number, message_url)
    return result

with gr.Blocks() as interface:
    gr.Markdown("## Prank Call AI Service")
    phone_number_input = gr.Textbox(label="Enter Phone Number")
    call_button = gr.Button("Initiate Call")
    call_output = gr.Textbox(label="Call Status")

    call_button.click(fn=make_call, inputs=phone_number_input, outputs=call_output)

    audio_url_input = gr.Textbox(label="Enter Audio URL")
    transcribe_button = gr.Button("Start Transcription")
    transcription_output = gr.Textbox(label="Transcription Status")

    transcribe_button.click(fn=start_transcription, inputs=audio_url_input, outputs=transcription_output)

    text_input = gr.Textbox(label="Enter Text")
    tts_button = gr.Button("Convert to Speech")
    tts_output = gr.Textbox(label="TTS Status")

    tts_button.click(fn=text_to_speech_conversion, inputs=text_input, outputs=tts_output)

    ai_text_input = gr.Textbox(label="Enter Text for AI Response")
    ai_button = gr.Button("Get AI Response")
    ai_output = gr.Textbox(label="AI Response")

    ai_button.click(fn=ai_response, inputs=ai_text_input, outputs=ai_output)

interface.launch()
