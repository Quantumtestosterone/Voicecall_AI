# Prank Call AI Service

This project implements a prank call AI service using various APIs and technologies.

## Setup

1. Install dependencies:
pip install -r requirements.txt
2. Set up environment variables in a `.env` file:
GROQ_API_KEY=your_groq_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=your_elevenlabs_voice_id
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
DG_API_KEY=your_deepgram_api_key
3. Run the main application:
python main.py
4. Run the server:
python server.py
## Project Structure

- `main.py`: Gradio interface for the prank call service
- `server.py`: Flask server for handling Twilio webhooks
- `api/`: Contains modules for interacting with various APIs
- `config.py`: Centralized configuration management
- `utils.py`: Utility functions and base classes
- `tests/`: Unit tests for each module
- `docs/`: Project documentation

## Features

- Initiate phone calls using Twilio
- Transcribe audio using Deepgram
- Generate AI responses using Groq
- Convert text to speech using ElevenLabs

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.