import gradio as gr
import asyncio
import logging
import os
import json
import threading
from api.phone_call import test_twilio_connection, initiate_call
from api.deepgram_transcription import start_deepgram_transcription
from api.text_to_speech import convert_text_to_speech
from api.ai_model import get_ai_response, set_ai_model
from config import Config
from server import app as flask_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_api_keys(groq_api_key, elevenlabs_api_key, elevenlabs_voice_id, 
                  twilio_account_sid, twilio_auth_token, twilio_api_key, twilio_api_secret, twilio_phone_number, 
                  deepgram_api_key, anthropic_api_key):
    Config.GROQ_API_KEY = groq_api_key
    Config.ELEVENLABS_API_KEY = elevenlabs_api_key
    Config.ELEVENLABS_VOICE_ID = elevenlabs_voice_id
    Config.TWILIO_ACCOUNT_SID = twilio_account_sid
    Config.TWILIO_AUTH_TOKEN = twilio_auth_token
    Config.TWILIO_API_KEY = twilio_api_key
    Config.TWILIO_API_SECRET = twilio_api_secret
    Config.TWILIO_PHONE_NUMBER = twilio_phone_number
    Config.DEEPGRAM_API_KEY = deepgram_api_key
    Config.ANTHROPIC_API_KEY = anthropic_api_key
    
    Config.save_to_file()
    
    return "API keys saved successfully!"

def save_api_keys_to_desktop(groq_api_key, elevenlabs_api_key, elevenlabs_voice_id, 
                             twilio_account_sid, twilio_auth_token, twilio_api_key, twilio_api_secret, twilio_phone_number, 
                             deepgram_api_key, anthropic_api_key):
    config_data = {
        "GROQ_API_KEY": groq_api_key,
        "ELEVENLABS_API_KEY": elevenlabs_api_key,
        "ELEVENLABS_VOICE_ID": elevenlabs_voice_id,
        "TWILIO_ACCOUNT_SID": twilio_account_sid,
        "TWILIO_AUTH_TOKEN": twilio_auth_token,
        "TWILIO_API_KEY": twilio_api_key,
        "TWILIO_API_SECRET": twilio_api_secret,
        "TWILIO_PHONE_NUMBER": twilio_phone_number,
        "DEEPGRAM_API_KEY": deepgram_api_key,
        "ANTHROPIC_API_KEY": anthropic_api_key
    }
    
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop_path, "ai_call_service_config.json")
    
    with open(file_path, 'w') as f:
        json.dump(config_data, f, indent=4)
    
    return f"API keys saved to {file_path}"

def load_api_keys_from_file():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop_path, "ai_call_service_config.json")
    
    try:
        with open(file_path, 'r') as f:
            config_data = json.load(f)
        
        Config.GROQ_API_KEY = config_data.get("GROQ_API_KEY", "")
        Config.ELEVENLABS_API_KEY = config_data.get("ELEVENLABS_API_KEY", "")
        Config.ELEVENLABS_VOICE_ID = config_data.get("ELEVENLABS_VOICE_ID", "")
        Config.TWILIO_ACCOUNT_SID = config_data.get("TWILIO_ACCOUNT_SID", "")
        Config.TWILIO_AUTH_TOKEN = config_data.get("TWILIO_AUTH_TOKEN", "")
        Config.TWILIO_API_KEY = config_data.get("TWILIO_API_KEY", "")
        Config.TWILIO_API_SECRET = config_data.get("TWILIO_API_SECRET", "")
        Config.TWILIO_PHONE_NUMBER = config_data.get("TWILIO_PHONE_NUMBER", "")
        Config.DEEPGRAM_API_KEY = config_data.get("DEEPGRAM_API_KEY", "")
        Config.ANTHROPIC_API_KEY = config_data.get("ANTHROPIC_API_KEY", "")
        
        Config.save_to_file()
        
        return ("API keys loaded successfully!", 
                Config.GROQ_API_KEY, Config.ELEVENLABS_API_KEY, Config.ELEVENLABS_VOICE_ID,
                Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN, Config.TWILIO_API_KEY,
                Config.TWILIO_API_SECRET, Config.TWILIO_PHONE_NUMBER, Config.DEEPGRAM_API_KEY,
                Config.ANTHROPIC_API_KEY)
    except FileNotFoundError:
        return ("Config file not found on desktop.", "", "", "", "", "", "", "", "", "", "")
    except json.JSONDecodeError:
        return ("Error reading config file. Invalid JSON.", "", "", "", "", "", "", "", "", "", "")

def load_api_keys():
    Config.load_from_file()
    return (Config.GROQ_API_KEY or "", 
            Config.ELEVENLABS_API_KEY or "", 
            Config.ELEVENLABS_VOICE_ID or "", 
            Config.TWILIO_ACCOUNT_SID or "", 
            Config.TWILIO_AUTH_TOKEN or "", 
            Config.TWILIO_API_KEY or "", 
            Config.TWILIO_API_SECRET or "", 
            Config.TWILIO_PHONE_NUMBER or "", 
            Config.DEEPGRAM_API_KEY or "", 
            Config.ANTHROPIC_API_KEY or "")

def create_interface() -> gr.Blocks:
    with gr.Blocks() as interface:
        gr.Markdown("## AI Call Service")
        
        with gr.Tab("Setup"):
            groq_api_key = gr.Textbox(label="Groq API Key", type="password")
            elevenlabs_api_key = gr.Textbox(label="ElevenLabs API Key", type="password")
            elevenlabs_voice_id = gr.Textbox(label="ElevenLabs Voice ID")
            twilio_account_sid = gr.Textbox(label="Twilio Account SID", type="password")
            twilio_auth_token = gr.Textbox(label="Twilio Auth Token", type="password")
            twilio_api_key = gr.Textbox(label="Twilio API Key", type="password")
            twilio_api_secret = gr.Textbox(label="Twilio API Secret", type="password")
            twilio_phone_number = gr.Textbox(label="Twilio Phone Number")
            deepgram_api_key = gr.Textbox(label="Deepgram API Key", type="password")
            anthropic_api_key = gr.Textbox(label="Anthropic API Key", type="password")
            
            with gr.Row():
                save_button = gr.Button("Save API Keys")
                save_to_desktop_button = gr.Button("Save API Keys to Desktop")
                load_from_desktop_button = gr.Button("Load API Keys from Desktop")
            
            save_output = gr.Textbox(label="Save/Load Status")
            
            save_button.click(fn=save_api_keys, 
                              inputs=[groq_api_key, elevenlabs_api_key, elevenlabs_voice_id, 
                                      twilio_account_sid, twilio_auth_token, twilio_api_key, twilio_api_secret, twilio_phone_number, 
                                      deepgram_api_key, anthropic_api_key], 
                              outputs=save_output)
            
            save_to_desktop_button.click(fn=save_api_keys_to_desktop,
                                         inputs=[groq_api_key, elevenlabs_api_key, elevenlabs_voice_id, 
                                                 twilio_account_sid, twilio_auth_token, twilio_api_key, twilio_api_secret, twilio_phone_number, 
                                                 deepgram_api_key, anthropic_api_key], 
                                         outputs=save_output)
            
            load_from_desktop_button.click(fn=load_api_keys_from_file,
                                           outputs=[save_output, 
                                                    groq_api_key, elevenlabs_api_key, elevenlabs_voice_id, 
                                                    twilio_account_sid, twilio_auth_token, twilio_api_key, twilio_api_secret, twilio_phone_number, 
                                                    deepgram_api_key, anthropic_api_key])

        with gr.Tab("Test Connections"):
            test_twilio_button = gr.Button("Test Twilio Connection")
            test_twilio_output = gr.Textbox(label="Twilio Test Result")
            test_twilio_button.click(fn=test_twilio_connection, outputs=test_twilio_output)

        with gr.Tab("Initiate Call"):
            phone_number_input = gr.Textbox(label="Enter Phone Number")
            call_button = gr.Button("Initiate Call")
            call_output = gr.Textbox(label="Call Status")
            call_button.click(fn=lambda phone: asyncio.run(initiate_call(phone)), inputs=phone_number_input, outputs=call_output)

        with gr.Tab("Transcription"):
            audio_file_input = gr.File(label="Upload Audio File")
            transcribe_button = gr.Button("Start Transcription")
            transcription_output = gr.Textbox(label="Transcription Result")
            transcribe_button.click(fn=lambda file: asyncio.run(start_deepgram_transcription(file)), 
                                    inputs=audio_file_input, 
                                    outputs=transcription_output)

        with gr.Tab("Text to Speech"):
            text_input = gr.Textbox(label="Enter Text")
            tts_button = gr.Button("Convert to Speech")
            tts_output = gr.Audio(label="TTS Output")
            tts_button.click(fn=lambda text: asyncio.run(convert_text_to_speech(text)), 
                             inputs=text_input, 
                             outputs=tts_output)

        with gr.Tab("AI Response"):
            ai_model_selection = gr.Dropdown(label="Select AI Model", choices=["Groq", "Claude 3.5 Sonnet"], value="Groq")
            system_prompt = gr.Textbox(label="System Prompt", value="You are an AI designed to engage in phone calls.")
            ai_text_input = gr.Textbox(label="Enter Text for AI Response")
            ai_button = gr.Button("Get AI Response")
            ai_output = gr.Textbox(label="AI Response")
            ai_button.click(fn=lambda model, prompt, text: asyncio.run(get_ai_response(set_ai_model(model), prompt, text)),
                            inputs=[ai_model_selection, system_prompt, ai_text_input],
                            outputs=ai_output)

        interface.load(fn=load_api_keys, outputs=[
            groq_api_key, elevenlabs_api_key, elevenlabs_voice_id, 
            twilio_account_sid, twilio_auth_token, twilio_api_key, twilio_api_secret, twilio_phone_number, 
            deepgram_api_key, anthropic_api_key
        ])

    return interface

def run_flask_server():
    flask_app.run(port=5000)

if __name__ == "__main__":
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask_server)
    flask_thread.start()

    # Run Gradio interface
    interface = create_interface()
    interface.launch(debug=True)