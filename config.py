from google.oauth2 import service_account

import os
import logging

CREDS = os.getenv("CREDS")
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
            creds = service_account.Credentials.from_service_account_file(
                 CREDS, scopes=SCOPES)                       
            return creds
        except TypeError as e :
            logging.info(f"TypeError {e}")