from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from api.deepgram_transcription import start_deepgram_transcription
from api.text_to_speech import convert_text_to_speech
from api.ai_model import get_ai_response, set_ai_model
from config import Config

app = Flask(__name__)

@app.route("/message", methods=["POST"])
async def message():
    response = VoiceResponse()
    gather = Gather(input="speech", action="/handle_speech", method="POST")
    gather.say("Hello, this is a call service. Please say something.")
    response.append(gather)
    return str(response)

@app.route("/handle_speech", methods=["POST"])
async def handle_speech():
    speech_result = request.form['SpeechResult']
    
    # Use a specific AI model (e.g., Claude)
    ai_client = set_ai_model("Claude 3.5 Sonnet")
    system_prompt = "You are an AI designed to engage in phone calls."
    
    ai_reply = await get_ai_response(ai_client, system_prompt, speech_result)
    tts_response = await convert_text_to_speech(ai_reply)

    response = VoiceResponse()
    response.play(tts_response)
    return str(response)

if __name__ == "__main__":
    app.run(port=5000)