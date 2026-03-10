# AI Receptionist (Flask + Twilio)

Minimal scaffold for an AI receptionist using Flask for webhooks, Twilio for SMS/Voice, and optional OpenAI for smart replies.

## Files
- `app.py` — Flask app with `/sms`, `/voice`, and recording callback endpoints.
- `openai_client.py` — Generates replies via OpenAI (if `OPENAI_API_KEY` set) or fallback rules.
- `twilio_client.py` — Simple Twilio REST helper for notifications.
- `templates/index.html` — Basic homepage.
- `.env.example` — Example env vars.
- `requirements.txt` — Python dependencies.

## Setup

1. Create and activate a virtual environment, then install:
```bash
python -m venv .venv
.venv\\Scripts\\activate    # Windows
pip install -r requirements.txt