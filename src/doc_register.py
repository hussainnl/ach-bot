import sys
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import Configuration 



def doc_register(doc_id,massage):
    print("--- 3. دخلنا إلى دالة main ---")
    massage = massage
    creds = None
    try:
        print("--- 4. جارٍ محاولة المصادقة (authenticate_google) ---")
        creds = Configuration().authenticate_google()
        if creds:
            print("--- 5. تمت المصادقة بنجاح، حصلنا على creds ---")
        else:
            # إذا كانت authenticate_google() قد تعيد None في حالة الفشل
            print("--- 5. فشلت المصادقة، لم يتم إرجاع creds! ---")
            sys.exit(1) # الخروج من البرنامج

    except Exception as e:
        print(f"!!! حدث خطأ أثناء المصادقة: {e}")
        sys.exit(1)


    try:
        print("--- 6. جارٍ بناء خدمة Google Docs (build service) ---")
        service = build("docs", "v1", credentials=creds)
        print("--- 7. تم بناء الخدمة بنجاح ---")

        requests = [
            {
                'insertText': {
                    'location': { 'index': 1 },
                    'text': f"{massage}\n"
                }
            },
        ]

        print("--- 8. سيتم الآن تنفيذ طلب batchUpdate ---")
        result = service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests}
        ).execute()
        print("--- 9. تم تنفيذ طلب batchUpdate بنجاح! ---")
        print(f"النتيجة: {result}")

    except HttpError as err:
        print(f"!!! حدث خطأ من Google API: {err}")
    except Exception as e:
        print(f"!!! حدث خطأ غير متوقع: {e}")

# --- بداية تنفيذ البرنامج ---

