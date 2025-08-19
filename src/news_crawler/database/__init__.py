from supabase import create_client, Client, ClientOptions
from datetime import datetime
from common.config import Config

supabase: Client = create_client(
    Config.supabase_url,
    Config.supabase_key 
)

def upsert_cosmetic_news(news: dict):
    try:
        news["updated_at"] = datetime.now().isoformat()
        response = supabase.table("cosmetic_news").upsert(news).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error upserting category '{news.get('title', 'unknown')}': {e}")
        return None
    
def get_cosmetic_news(company: str, start: int, limit: int):
    try:
        response = supabase.table('cosmetic_news').select("*").eq("company", company).range(start, start + limit).execute()
        return response.data if response.data else []
    except Exception as e:
        return []

def get_cosmetic_news_with_link(company: str, url: str):
    try:
        response = supabase.table('cosmetic_news').select("*").eq("company", company).eq("url", url).execute()
        return response.data if response.data else []
    except Exception as e:
        return []
    
def get_relevant_cosmetic_news(company: str, start: int, limit: int):
    try:
        response = supabase.table('cosmetic_news').select("*").eq("company", company).eq("relevant", 1).range(start, start + limit).execute()
        return response.data if response.data else []
    except Exception as e:
        return []

