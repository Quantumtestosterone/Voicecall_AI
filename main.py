import gradio as gr
import os
from api.phone_call import initiate_call
from api.deepgram_transcription import start_deepgram_transcription
from api.text_to_speech import convert_text_to_speech
from api.ai_model import get_ai_response, set_ai_model
from config import Config

def save_api_keys(groq_api_key, elevenlabs_api_key, elevenlabs_voice_id, twilio_account_sid, twilio_auth_token, twilio_phone_number, deepgram_api_key, anthropic_api_key):
    Config.GROQ_API_KEY = groq_api_key
    Config.ELEVENLABS_API_KEY = elevenlabs_api_key
    Config.ELEVENLABS_VOICE_ID = elevenlabs_voice_id
    Config.TWILIO_ACCOUNT_SID = twilio_account_sid
    Config.TWILIO_AUTH_TOKEN = twilio_auth_token
    Config.TWILIO_PHONE_NUMBER = twilio_phone_number
    Config.DEEPGRAM_API_KEY = deepgram_api_key
    Config.ANTHROPIC_API_KEY = anthropic_api_key
    
    # Save to .env file
    with open('.env', 'w') as f:
        f.write(f"GROQ_API_KEY={groq_api_key}\n")
        f.write(f"ELEVENLABS_API_KEY={elevenlabs_api_key}\n")
        f.write(f"ELEVENLABS_VOICE_ID={elevenlabs_voice_id}\n")
        f.write(f"TWILIO_ACCOUNT_SID={twilio_account_sid}\n")
        f.write(f"TWILIO_AUTH_TOKEN={twilio_auth_token}\n")
        f.write(f"TWILIO_PHONE_NUMBER={twilio_phone_number}\n")
        f.write(f"DG_API_KEY={deepgram_api_key}\n")
        f.write(f"ANTHROPIC_API_KEY={anthropic_api_key}\n")
    
    return "API keys saved successfully!"

def create_interface() -> gr.Blocks:
    with gr.Blocks() as interface:
        gr.Markdown("## Prank Call AI Service")
        
        with gr.Tab("Setup"):
            groq_api_key = gr.Textbox(label="Groq API Key", type="password")
            elevenlabs_api_key = gr.Textbox(label="ElevenLabs API Key", type="password")
            elevenlabs_voice_id = gr.Textbox(label="ElevenLabs Voice ID")
            twilio_account_sid = gr.Textbox(label="Twilio Account SID", type="password")
            twilio_auth_token = gr.Textbox(label="Twilio Auth Token", type="password")
            twilio_phone_number = gr.Textbox(label="Twilio Phone Number")
            deepgram_api_key = gr.Textbox(label="Deepgram API Key", type="password")
            anthropic_api_key = gr.Textbox(label="Anthropic API Key", type="password")
            save_button = gr.Button("Save API Keys")
            save_output = gr.Textbox(label="Save Status")
            
            save_button.click(fn=save_api_keys, 
                              inputs=[groq_api_key, elevenlabs_api_key, elevenlabs_voice_id, 
                                      twilio_account_sid, twilio_auth_token, twilio_phone_number, 
                                      deepgram_api_key, anthropic_api_key], 
                              outputs=save_output)
        
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
            voice_selection = gr.Dropdown(label="Select Voice", choices=["ElevenLabs"], value="ElevenLabs")
            tts_button = gr.Button("Convert to Speech")
            tts_output = gr.Audio(label="TTS Output")
            tts_button.click(fn=convert_text_to_speech, inputs=[text_input, voice_selection], outputs=tts_output)

        with gr.Tab("AI Response"):
            ai_model_selection = gr.Dropdown(label="Select AI Model", choices=["Groq", "Claude 3.5 Sonnet"], value="Groq")
            system_prompt = gr.Textbox(label="System Prompt", value="You are an AI designed to engage in prank calls.")
            ai_text_input = gr.Textbox(label="Enter Text for AI Response")
            ai_button = gr.Button("Get AI Response")
            ai_output = gr.Textbox(label="AI Response")
            ai_button.click(fn=lambda model, prompt, text: get_ai_response(set_ai_model(model), prompt, text), 
                            inputs=[ai_model_selection, system_prompt, ai_text_input], 
                            outputs=ai_output)

    return interface

if __name__ == "__main__":
    interface = create_interface()
    interface.launch()