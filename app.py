import os
from flask import Flask, request, render_template, url_for
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
from dotenv import load_dotenv
from openai_client import generate_reply
from twilio_client import send_sms_notification

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming = request.form.get("Body", "")
    from_number = request.form.get("From", "")
    # generate reply (uses OpenAI if configured, otherwise fallback)
    reply_text = generate_reply(incoming, from_number)
    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp), 200, {"Content-Type": "application/xml"}

@app.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()
    resp.say("Hello. You have reached our AI receptionist. Please leave a message after the beep.")
    resp.record(max_length=120, play_beep=True, action=url_for("handle_recording", _external=True))
    resp.say("Thank you. Goodbye.")
    return str(resp), 200, {"Content-Type": "application/xml"}

@app.route("/voice/recording", methods=["POST"])
def handle_recording():
    recording_url = request.form.get("RecordingUrl")
    from_number = request.form.get("From")
    # Notify staff via SMS (if Twilio creds configured)
    if from_number and recording_url:
        body = f"New voicemail from {from_number}: {recording_url}"
        try:
            send_sms_notification(body)
        except Exception:
            pass
    resp = VoiceResponse()
    resp.say("Thanks — your message has been recorded.")
    return str(resp), 200, {"Content-Type": "application/xml"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)