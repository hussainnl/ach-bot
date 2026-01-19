from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import logging

CREDS = os.getenv("CREDS")
TOKEN = os.getenv("TOKEN")
SCOPE = os.getenv("SCOPES")
SCOPES = []
SCOPES.append(SCOPE)
print(SCOPES)
class Configuration:

    def __init__(self):
        pass
    
    def authenticate_google(self):
        """
        دالة المصادقة الموحدة (تعمل مع Drive و Gmail)
        """
        try:
            creds = None
            if os.path.exists(TOKEN):
                creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    # تذكر حذف token.json بعد تغيير الـ SCOPES
                    flow = InstalledAppFlow.from_client_secrets_file(
                        CREDS, SCOPES)
                    creds = flow.run_local_server(port=0)
                with open(TOKEN, 'w') as token:
                    token.write(creds.to_json())
            return creds
        except TypeError as e :
            logging.info(f"TypeError {e}")