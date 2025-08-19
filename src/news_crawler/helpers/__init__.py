from lib.google_search import search_from_google
from helpers.scrap import scrap_news
from helpers.ai_func import generate_summary, check_relevant_news, check_duplicated_news
from database import upsert_cosmetic_news, get_cosmetic_news_with_link

def process_company_news(company_name: str):
    summary_list = []
    
    for i in range(0, 100, 10):
        results = search_from_google(company_name, i)
        if len(results) == 0:
            break

        for result in results:
            title = result.get("title", "")
            link = result.get("link", "")
            print(title)

            if get_cosmetic_news_with_link(company_name, link):
                continue

            body = scrap_news(link)
            summary_set = generate_summary(body)

            published_at = summary_set.get("일자", "")
            press = summary_set.get("언론사", "")
            author = summary_set.get("기고자", "")
            content = summary_set.get("본문", "")
            url = link
            category = summary_set.get("기사 카테고리", "")
            summary = summary_set.get("핵심 메시지", "")
            keywords = summary_set.get("키워드", [])

            # TODO: 연관성 높은 뉴스를 필터링
            if not check_relevant_news(company_name, title, summary):
                continue

            # TODO: 중복 기사 제거
            if check_duplicated_news(summary_list, summary):
                continue

            summary_list.append(summary)

            try:
                record = {
                    "company": company_name,
                    "published_at": published_at,
                    "press": press,
                    "author": author,
                    "title": title,
                    "content": content,
                    "url": url,
                    "category": category,
                    "summary": summary,
                    "keywords": keywords,
                    "relevant": 1,
                }
                upsert_cosmetic_news(record)
                print(f"Upserted record {record}")
            except Exception as e:
                print(f"Error upserting record for code {title}: {e}")
            

        
        
        
        