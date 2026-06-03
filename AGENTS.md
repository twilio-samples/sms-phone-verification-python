# Build a User Registration System with SMS Phone Verification

A Flask application demonstrating user registration, authentication, and SMS phone verification using Twilio Verify.

## Commands

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install
pip install -r requirements.txt

# Run
python app.py
```

## Environment Variables

Copy `.env.example` to `.env`. Never commit `.env`.

```bash
cp .env.example .env
```

| Variable | Where to find | Format |
| -------- | ------------- | ------ |
| `TWILIO_ACCOUNT_SID` | [Console](https://console.twilio.com) homepage | Starts with `AC` |
| `TWILIO_AUTH_TOKEN` | Console homepage → click to reveal | 32-char string. Treat as a password. |
| `VERIFY_SERVICE_SID` | Console → Verify → Services | Starts with `VA` |
| `SECRET_KEY` | Generate any random string | Used for Flask session signing |
| `PORT` | Optional | Defaults to `5000` |

## Project Structure

- `app.py` — Flask application with routes and database setup
- `templates/` — Jinja2 templates (register, login, verify, dashboard)
- `static/css/paste.css` — Twilio Paste-inspired styling

## Agent Boundaries

**Always:**
- Confirm `.env` is configured before running any command
- Use the Environment Variables section to guide the user to each credential — don't ask them to find values without direction
- Confirm the app is running before asking the user to test it

**Never:**
- Run the app with missing or placeholder credentials
- Hardcode credentials or phone numbers in source files
- Skip the `cp .env.example .env` step

## Verify It's Working

1. Open http://localhost:5000 and register a new account with your phone number
2. Click "Send Verification Code" — you should receive an SMS with a 6-digit code
3. Enter the code and click "Verify Code" — you should see the verified dashboard

## Twilio Resources

- [Twilio Console](https://console.twilio.com) — credentials, phone numbers, webhook configuration
- [Twilio Verify Documentation](https://www.twilio.com/docs/verify)
- [Twilio Python SDK](https://www.twilio.com/docs/libraries/reference/twilio-python)
