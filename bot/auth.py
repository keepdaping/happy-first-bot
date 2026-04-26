import json
import os
from playwright.sync_api import sync_playwright
from .config import HEADLESS_MODE

SESSION_FILE = os.path.join(os.path.dirname(__file__), "..", "session.json")


def login():
    with open(SESSION_FILE, "r") as f:
        data = json.load(f)

    # session.json may be a bare list or {"cookies": [...]}
    if isinstance(data, list):
        cookies = data
    elif isinstance(data, dict) and "cookies" in data:
        cookies = data["cookies"]
    else:
        raise Exception("session.json must be a list of cookies or {\"cookies\": [...]}")

    if not isinstance(cookies, list):
        raise Exception("session.json must be a list of cookies")

    # Add url field to each cookie (required by Playwright)
    # Keep only required fields: name, value, url
    cleaned_cookies = []
    for cookie in cookies:
        cleaned = {
            "name": cookie.get("name"),
            "value": cookie.get("value"),
            "url": "https://x.com"
        }
        cleaned_cookies.append(cleaned)
    
    cookies = cleaned_cookies

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=HEADLESS_MODE)
    context = browser.new_context()

    page = context.new_page()
    # First navigate to x.com
    page.goto("https://x.com", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    
    # Add cookies after navigation
    print(f"[auth] loading {len(cookies)} cookies")
    context.add_cookies(cookies)

    # Now navigate to home
    page.goto("https://x.com/home", wait_until="domcontentloaded")
    page.wait_for_timeout(5000)

    print(f"[auth] current URL: {page.url}")

    return playwright, browser, page
