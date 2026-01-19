from google.oauth2.credentials import Credentials 
from google.oauth2 import service_account 
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
            creds = service_account.Credentials.from_service_account_file(CREDS,scopes = SCOPES)
            # if not creds or not creds.valid:
            #     if creds and creds.expired and creds.refresh_token:
            #         creds.refresh(Request())
            #     else:
            #         # تذكر حذف token.json بعد تغيير الـ SCOPES
            #         flow = InstalledAppFlow.from_client_secrets_file(
            #             CREDS, SCOPES)
            #         creds = flow.run_local_server(port=0)
            return creds
        except TypeError as e :
            logging.info(f"TypeError {e}")