import logging
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TwilioClient:
    def __init__(self):
        self.account_sid = Config.TWILIO_ACCOUNT_SID
        self.auth_token = Config.TWILIO_AUTH_TOKEN
        self.phone_number = Config.TWILIO_PHONE_NUMBER
        self.api_key = Config.TWILIO_API_KEY
        self.api_secret = Config.TWILIO_API_SECRET
        self._client = None

    @property
    def client(self):
        if self._client is None:
            if self.api_key and self.api_secret:
                logger.info("Initializing Twilio client with API Key and Secret")
                self._client = Client(self.api_key, self.api_secret, self.account_sid)
            else:
                logger.info("Initializing Twilio client with Account SID and Auth Token")
                self._client = Client(self.account_sid, self.auth_token)
        return self._client

    def test_connection(self):
        try:
            logger.info(f"Testing Twilio connection with Account SID: {self.account_sid}")
            account = self.client.api.accounts(self.account_sid).fetch()
            logger.info(f"Twilio connection successful. Account status: {account.status}")
            return f"Twilio connection successful. Account status: {account.status}"
        except TwilioRestException as e:
            logger.error(f"Twilio connection failed: {str(e)}\nError code: {e.code}\nError message: {e.msg}")
            return f"Twilio connection failed: {str(e)}\nError code: {e.code}\nError message: {e.msg}"
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return f"Unexpected error: {str(e)}"

    async def initiate_call(self, to_phone_number: str, message_url: str) -> str:
        try:
            call = self.client.calls.create(
                to=to_phone_number,
                from_=self.phone_number,
                url=message_url
            )
            return f"Call initiated with SID: {call.sid}"
        except Exception as e:
            logger.error(f"Error initiating call: {str(e)}")
            return f"Error initiating call: {str(e)}"

def test_twilio_connection():
    client = TwilioClient()
    return client.test_connection()

async def initiate_call(to_phone_number: str) -> str:
    message_url = "http://your-server-url/message"  # Placeholder URL for Twilio to fetch instructions
    client = TwilioClient()
    return await client.initiate_call(to_phone_number, message_url)