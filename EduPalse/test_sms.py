from twilio.rest import Client

client = Client("AC62a24686fc5a488c0fd9dc67846ea823", "d51b7c66e857f8ee2bdbb5bc687710fb")

message = client.messages.create(
    body="Hello! This is a test from Twilio WhatsApp.",
    from_="+14155238886",
    to="+919865864986"
)
