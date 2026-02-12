from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import Configuration 
import logging


def doc_register(doc_id,massage): 
    """to register the user achievements message in google doc"""
    
    massage = massage
    creds = None
    try:
        
        creds = Configuration().authenticate_google()
        if creds == None:
            logging.info(f"creds = None")


    except Exception as e:
        logging.info(f"Error {e}")
        


    try:
        service = build("docs", "v1", credentials=creds)
        requests = [
            {
                'insertText': {
                    'location': { 'index': 1 },
                    'text': f"{massage}\n"
                }
            },
        ]

        service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests}
        ).execute()
 
    except HttpError as err:
        print(f"!!! Error in Google API: {err}")
    except Exception as e:
        print(f"!!! Error : {e}")

