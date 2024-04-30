from twilio.rest import Client

# Your Twilio Account SID, Auth Token, and Twilio phone number
account_sid = 'sid'
auth_token = 'ath'
twilio_phone_number = 'phno'

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Send SMS
def send_sms(message, to_phone_number="+918277638169"):
    client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=to_phone_number
    )

# Example usage
ph="+918277638169"
send_sms("Loitering activity detected!", ph)



