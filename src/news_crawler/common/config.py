from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    naver_api_client_id: str = os.getenv("NAVER_API_CLIENT_ID", "")
    naver_api_client_secret: str = os.getenv("NAVER_API_CLIENT_SECRET", "")
    google_api_key: str = os.getenv("GOOGLE_SEARCH_API_KEY", "")
    google_cx: str = os.getenv("GOOGLE_SEARCH_CX", "")
    supabase_url: str = os.getenv("SUPABASE_URL")
    supabase_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    def __init__(self):
        pass   