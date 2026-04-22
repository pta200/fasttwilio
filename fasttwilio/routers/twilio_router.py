import os

from fastapi import APIRouter, HTTPException, Response
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")
twilio_client = Client(account_sid, auth_token)


twilio_router = APIRouter(
    prefix="/twilio", tags=["sms, email"], responses={404: {"description": "not found"}}
)


@twilio_router.post("/reply_sms")
async def reply_sms():
    # Create a new Twilio MessagingResponse
    resp = MessagingResponse()
    resp.message("The Robots are coming! Head for the hills!")

    # Return the TwiML (as XML) response
    return Response(str(resp), mimetype="text/xml")


@twilio_router.post("/semd_sms")
async def send_sms():
    try:
        message = twilio_client.messages.create(
            body="Join Earth's mightiest heroes. Like Kevin Bacon.",
            from_="+15017122661",
            to="+15558675310",
        )

        return Response(str(message))
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from Exception
