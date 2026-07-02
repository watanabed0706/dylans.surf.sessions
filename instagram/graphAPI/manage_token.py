import os
import sys
from dotenv import load_dotenv
import time
import requests

load_dotenv()
ACCESS_TOKEN = os.environ['IG_ACCESS_TOKEN']
IG_USER_ID = os.environ['IG_USER_ID']

# Check if Token is Valid

# Refresh Token (if possible)

# Generate New Token (if none or expired)
# Might require some sort of hosting/UI to streamline
#       Ngrok?