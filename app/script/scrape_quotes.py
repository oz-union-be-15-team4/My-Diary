import asyncio
import re
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import requests
from bs4 import BeautifulSoup
from tortoise import Tortoise
from dotenv import load_dotenv
import os

from app.models.quote import Quote

load_dotenv()

DB_URL = (
    f"postgres://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)


def parse_title(title_text: str):
    if " - " in title_text:
        parts = title_text.split(" - ", 1)
        category = parts[0].strip()
        author = parts[1].strip()
        return category, author
    else:
        return None, title_text.strip()


def extract_author_from_content(content: str):
    lines = content.split('\n')
    for line in reversed(lines):
        line = line.strip()
        if line.startswith('-'):
            author = line[1:].strip()
            if author:
                return author
    return None


def clean_content(content: str):
    content = re.sub(r'<[^>]+>', '', content)
    content = content.replace('&#039;', "'")
    content = content.replace('&quot;', '"')
    content = content.replace('&amp;', '&')
    content = content.replace('&lt;', '<')
    content = content.replace('&gt;', '>')
    content = re.sub(r'\s+', ' ', content)
    content = content.strip()
    return content


async def scrape_quotes_from_page(url: str, page_num: int = 1):
    if page_num > 1:
        url = f"{url}?page={page_num}"
    
    print(f"스크래핑 중: {url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = []
        
        table = soup.find('table')
        if not table:
            print(f"테이블을 찾을 수 없습니다: {url}")
            return quotes
        
        tbody = table.find('tbody')
        if not tbody:
            print(f"테이블 본문을 찾을 수 없습니다: {url}")
            return quotes
        
        rows = tbody.find_all('tr')
        
        i = 0
        while i < len(rows):
            row = rows[i]
            
            title_cell = row.find('td', class_='td_subject')
            if title_cell:
                title_link = title_cell.find('a')
                if title_link:
                    title_text = title_link.get_text(strip=True)
                    source_url = title_link.get('href', '')
                    
                    if source_url and not source_url.startswith('http'):
                        source_url = f"https://saramro.com{source_url}"
                    
                    if i + 1 < len(rows):
                        content_row = rows[i + 1]
                        content_cell = content_row.find('td', colspan='5')
                        if content_cell:
                            content = content_cell.get_text(separator='\n', strip=True)
                            content = clean_content(content)
                            
                            category, author_from_title = parse_title(title_text)
                            
                            author_from_content = extract_author_from_content(content)
                            
                            author = author_from_content or author_from_title
                            
                            if author_from_content:
                                lines = content.split('\n')
                                if lines and lines[-1].strip().startswith('-'):
                                    content = '\n'.join(lines[:-1]).strip()
                            
                            if content:
                                quotes.append({
                                    'title': title_text,
                                    'content': content,
                                    'author': author,
                                    'category': category,
                                    'source_url': source_url
                                })
                    
                    i += 2
                else:
                    i += 1
            else:
                i += 1
        
        print(f"{len(quotes)}개의 명언을 찾았습니다.")
        return quotes
        
    except Exception as e:
        print(f"스크래핑 중 오류 발생: {e}")
        return []


async def save_quotes_to_db(quotes: list):
    saved_count = 0
    skipped_count = 0
    
    for quote_data in quotes:
        existing = None
        if quote_data.get('source_url'):
            existing = await Quote.filter(source_url=quote_data['source_url']).first()
        else:
            existing = await Quote.filter(
                title=quote_data['title'],
                content=quote_data['content']
            ).first()
        
        if existing:
            skipped_count += 1
            continue
        
        await Quote.create(
            title=quote_data['title'],
            content=quote_data['content'],
            author=quote_data.get('author'),
            category=quote_data.get('category'),
            source_url=quote_data.get('source_url')
        )
        saved_count += 1
    
    print(f"저장 완료: {saved_count}개, 건너뛴 항목: {skipped_count}개")


async def main():
    base_url = "https://saramro.com/quotes"
    
    print("데이터베이스 연결 중...")
    await Tortoise.init(
        db_url=DB_URL,
        modules={
            "models": ["app.models.quote"]
        },
    )
    
    try:
        total_quotes = []
        
        max_pages = 10
        
        for page in range(1, max_pages + 1):
            quotes = await scrape_quotes_from_page(base_url, page)
            if not quotes:
                print(f"{page}페이지에 더 이상 명언이 없습니다.")
                break
            
            total_quotes.extend(quotes)
            print(f"페이지 {page} 완료. 누적: {len(total_quotes)}개")
            
            await asyncio.sleep(1)
        
        print(f"\n총 {len(total_quotes)}개의 명언을 스크래핑했습니다.")
        
        if total_quotes:
            print("\n데이터베이스에 저장 중...")
            await save_quotes_to_db(total_quotes)
        
        print("\n스크래핑 완료!")
        
    finally:
        await Tortoise.close_connections()


async def run_quote_scraper():
    base_url = "https://saramro.com/quotes"

    await Tortoise.get_connection("default").execute_script(
        'TRUNCATE TABLE "quotes" RESTART IDENTITY;'
    )

    max_pages = 10

    for page in range(1, max_pages + 1):
        quotes = await scrape_quotes_from_page(base_url, page)
        if not quotes:
            print(f"{page}페이지에 더 이상 명언이 없습니다.")
            break

        print(f"{page}페이지에서 {len(quotes)}개 수집됨 → DB 저장 시작...")

        # 페이지에서 긁은 데이터 즉시 DB 저장
        await save_quotes_to_db(quotes)

        print(f"{page}페이지 저장 완료! (누적 저장 방식)")

        await asyncio.sleep(1)

    print("\n스크래핑 완료!")

if __name__ == "__main__":
    asyncio.run(main())
