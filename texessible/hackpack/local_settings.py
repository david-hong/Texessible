# Begin Heroku configuration - configured through environment variables.
import os
TWILIO_ACCOUNT_SID = os.environ.get('#', None)
TWILIO_AUTH_TOKEN = os.environ.get('#', None)
TWILIO_CALLER_ID = os.environ.get('#', None)
