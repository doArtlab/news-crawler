from news_crawler.helpers import process_company_news

if __name__ == "__main__":
    companies = [
        "코스맥스",
        "한국콜마",
        "아모레퍼시픽",
        "LG생활건강",
    ]

    for company in companies:
        print(f"Processing {company}..")
        process_company_news(company)