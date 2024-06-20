from twilio.rest import Client
from config import Config
from utils import BaseAPIClient, logger

class TwilioClient(BaseAPIClient):
    def __init__(self):
        super().__init__(Config.TWILIO_AUTH_TOKEN)
        self.account_sid = Config.TWILIO_ACCOUNT_SID
        self.phone_number = Config.TWILIO_PHONE_NUMBER
        self.client = Client(self.account_sid, self.api_key)

    async def initiate_call(self, to_phone_number: str, message_url: str) -> str:
        try:
            call = await self.client.calls.create(
                to=to_phone_number,
                from_=self.phone_number,
                url=message_url
            )
            return f"Call initiated with SID: {call.sid}"
        except Exception as e:
            return self.handle_error(e)

twilio_client = TwilioClient()

async def initiate_call(to_phone_number: str) -> str:
    message_url = "http://your-server-url/message"  # Placeholder URL for Twilio to fetch instructions
    return await twilio_client.initiate_call(to_phone_number, message_url)