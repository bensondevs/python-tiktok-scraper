import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from pprint import pprint
from urllib.parse import quote

from data.tiktok.tiktok_video_item import TikTokVideoItem

keyword = 'jakarta'.lower()
timestamp = int(time.time() * 1000)
search_url = f"https://www.tiktok.com/search/video?q={quote(keyword)}&t={timestamp}"

results = []

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)

    page = browser.new_page()
    page.goto(search_url)
    page.wait_for_selector(
        selector='[data-e2e="search_video-item-list"]',
        timeout=60000,
    )

    page.screenshot(path="screenshot.png")

    for _ in range(100):
        element_selector = '[data-e2e="search_video-item-list"]'
        page_html = page.query_selector(element_selector).inner_html()

        soup = BeautifulSoup(page_html, 'html.parser')
        video_items = soup.select('div[class*="DivItemContainerForSearch"]')

        for video_item in video_items:
            if video_item is None:
                continue

            image = video_item.find('img')

            results.append(
                TikTokVideoItem(
                    video_url=video_item.find('a')['href'],
                    thumbnail=image['src'],
                    caption=image['alt'],
                )
            )

        page.mouse.wheel(0, 10000)
        time.sleep(1)

    pprint(len(results))
    pprint(results)
