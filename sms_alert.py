from twilio.rest import Client

account_sid = 'YOUR_ACCOUNT_ID'
auth_token = 'YOUR_AUTH_TOKEN'
twilio_phone_number = 'YOUR_TWILIO PHONE_NUMBER'


client = Client(account_sid, auth_token)

# Send SMS
def send_sms(message, to_phone_number):
    client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=to_phone_number
    )

ph="+YOUR_PHONE_NUMBER"
flag=0
