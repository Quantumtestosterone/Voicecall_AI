import os
from flask import Flask, request
from dotenv import load_dotenv
from twilio.twiml.voice_response import VoiceResponse, Gather
from deepgram_transcription import start_deepgram_transcription
from text_to_speech import convert_text_to_speech
from ai_model import get_ai_response

load_dotenv()

app = Flask(__name__)

@app.route("/message", methods=["POST"])
def message():
    response = VoiceResponse()

    gather = Gather(input="speech", action="/handle_speech", method="POST")
    gather.say("Hello, this is a prank call service. Please say something.")
    response.append(gather)
    return str(response)

@app.route("/handle_speech", methods=["POST"])
def handle_speech():
    speech_result = request.form['SpeechResult']
    ai_reply = get_ai_response([
        {"role": "system", "content": "You are an AI designed to engage in prank calls."},
        {"role": "user", "content": speech_result},
    ])

    tts_response = convert_text_to_speech(ai_reply)

    response = VoiceResponse()
    response.play(tts_response)  # You need to handle the response to stream the audio file
    return str(response)

if __name__ == "__main__":
    app.run(port=5000)
