import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from voice_call_handler.voice.twilio_client import send_sms
import pytest

@pytest.mark.skipif(
    not (os.getenv("TWILIO_ACCOUNT_SID") and os.getenv("TWILIO_AUTH_TOKEN") and os.getenv("TWILIO_PHONE")),
    reason="Twilio credentials are not set in environment variables"
)
def test_send_sms():
    print("SID:", os.getenv("TWILIO_ACCOUNT_SID"))
    print("TOKEN:", os.getenv("TWILIO_AUTH_TOKEN"))
    print("PHONE:", os.getenv("TWILIO_PHONE"))
    sid = send_sms("+12675980303", "Ваш номер успешно забронирован.")
    assert sid is not None
    print("Message SID:", sid)
