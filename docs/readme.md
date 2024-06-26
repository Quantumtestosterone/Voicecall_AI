#  Call AI Service (Alpha Prototype)

**IMPORTANT NOTICE: This project is currently an alpha prototype and does not function as intended. It is a conceptual demonstration and should not be used for any real-world applications.**

## Project Overview

This project aims to implement a  call AI service using various APIs and technologies. It is designed to showcase the potential integration of multiple AI services for generating and conducting automated calls. However, please note that this is a work in progress and is not yet operational.

## Features (Planned)

- Initiate phone calls using Twilio
- Transcribe audio using Deepgram
- Generate AI responses using Groq or Anthropic's Claude 3.5 Sonnet
- Convert text to speech using ElevenLabs

## Setup

1. Clone this repository:
git clone (repo link)
cd repo

2. Create a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Run the main application:

5. Open the Gradio interface in your web browser (typically at http://127.0.0.1:7860).

6. Use the Setup tab in the Gradio interface to input your API keys and other necessary information.

## Project Structure

- `main.py`: Gradio interface for the  call service
- `server.py`: Flask server for handling Twilio webhooks
- `api/`: Contains modules for interacting with various APIs
- `config.py`: Centralized configuration management
- `utils.py`: Utility functions and base classes
- `tests/`: Unit tests for each module (not implemented yet)
- `docs/`: Project documentation

## Disclaimer

This project is a conceptual prototype and is not intended for actual use. Automated nk calls may be illegal in many jurisdictions and can cause distress to recipients. This project is for educational purposes only and should not be used to make real phone calls or harass individuals.

## Contributing

As this is an alpha prototype,  feel free to fork the repository and experiment with the concept on your own. Honestly, any help is appreciated 

## License

This project is licensed under the MIT License - see the LICENSE.md file for details. 

## Future Development

This prototype is a starting point for exploring the integration of various AI technologies. Future development may include:

- Implementing proper error handling and security measures
- Adding more AI model options
- Improving the user interface
- Developing a more robust backend architecture
- Ensuring compliance with relevant laws and ethical guidelines
- making the UI easier to work with
- reducing code to the bare minimum and optimizing inference
- adding scripts for the AI to stick with
- Agentic Framework
- Implementing Local Models for better cost efficiency (with elevenlabs its 8$ per hour of audio  which is too much)
- 

Please note that there are no concrete plans to develop this into a functional product at this time that said i'm always open to suggestions.
