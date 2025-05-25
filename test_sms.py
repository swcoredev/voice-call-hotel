from voice_call_handler.twilio_client import send_sms

sid = send_sms("+12675980303", "Ваш номер успешно забронирован.")
print("Message SID:", sid)
