# Prank Call AI Service

This project is a prank call AI service that uses Groqchat and Llama3 for fast AI model inference, Deepgram for fast speech-to-text conversion, and 11labs for text-to-speech conversion. The user interface is built with Gradio, and Twilio is used to make phone calls.

## Features

- **Speech-to-Text**: Converts speech to text using Deepgram.
- **Text-to-Speech**: Converts text to speech using 11labs.
- **AI Model**: Generates AI responses using Groqchat and Llama3.
- **Phone Call Integration**: Initiates phone calls using Twilio.
- **User Interface**: Allows users to input phone numbers and interact with the AI through a Gradio interface.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-username/prank-call-ai-service.git
    cd prank-call-ai-service
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `.env` file in the root directory of the project.
    - Add the following environment variables to the `.env` file:
        ```env
        DG_API_KEY=your_deepgram_api_key
        ELEVENLABS_API_KEY=your_elevenlabs_api_key
        GROQ_API_KEY=your_groq_api_key
        TWILIO_ACCOUNT_SID=your_twilio_account_sid
        TWILIO_AUTH_TOKEN=your_twilio_auth_token
        TWILIO_PHONE_NUMBER=your_twilio_phone_number
        ```

## Usage

1. **Run the Flask server**:
    ```sh
    python server.py
    ```

2. **Run the Gradio interface**:
    ```sh
    python main.py
    ```

3. **Access the Gradio interface**:
    - Open your web browser and go to the URL provided by Gradio (usually `http://127.0.0.1:7860`).

4. **Initiate a Call**:
    - Enter a phone number in the input field and click the "Initiate Call" button.

5. **Transcribe Audio**:
    - Enter an audio URL and click the "Start Transcription" button.

6. **Convert Text to Speech**:
    - Enter text in the input field and click the "Convert to Speech" button.

7. **Get AI Response**:
    - Enter text in the input field and click the "Get AI Response" button.

## Project Structure

- `main.py`: Gradio interface for user interaction.
- `deepgram_transcription.py`: Handles speech-to-text conversion using Deepgram.
- `text_to_speech.py`: Handles text-to-speech conversion using 11labs.
- `ai_model.py`: Generates AI responses using Groqchat and Llama3.
- `phone_call.py`: Initiates phone calls using Twilio.
- `server.py`: Flask server to handle Twilio webhooks and manage the conversation flow.

## Contributing

Feel free to submit issues, fork the repository and send pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
