from playwright.sync_api import Page
import time


def post_tweet(page: Page, text: str) -> bool:
    try:
        # Step 1: Navigate only if not already on home
        if "x.com/home" not in page.url:
            page.goto("https://x.com/home", wait_until="domcontentloaded")

        # Wait for page to be ready
        print("[tweet] waiting for page to load...")
        page.wait_for_selector('[data-testid="SideNav_NewTweet_Button"]', timeout=30000)
        print("[tweet] page loaded:", page.url)

        # Step 2: Click SideNav Post button to open compose
        page.locator('[data-testid="SideNav_NewTweet_Button"]').click()
        print("[tweet] clicked post button")

        # Step 3: Wait for compose — try both modal and inline testids
        textbox = None
        for sel in [
            '[data-testid="tweetTextarea_0"]',
            '[aria-label="Post text"]',
            'div[role="textbox"]',
            'div[contenteditable="true"]',
        ]:
            try:
                page.wait_for_selector(sel, state="attached", timeout=15000)
                textbox = page.locator(sel).first
                print(f"[tweet] textbox found: {sel}")
                break
            except Exception:
                continue

        # Step 4: If textbox not found, click the compose placeholder and retry
        if textbox is None:
            print("[tweet] activating compose by clicking placeholder area...")
            # Click the "What's happening?" text visible in the compose modal
            try:
                page.get_by_text("What's happening?").first.click(force=True)
            except Exception:
                page.mouse.click(575, 90)
            page.wait_for_timeout(3000)
            for sel in [
                '[data-testid="tweetTextarea_0"]',
                '[aria-label="Post text"]',
                'div[role="textbox"]',
                'div[contenteditable="true"]',
            ]:
                try:
                    page.wait_for_selector(sel, state="attached", timeout=8000)
                    textbox = page.locator(sel).first
                    print(f"[tweet] textbox after activate: {sel}")
                    break
                except Exception:
                    continue

        if textbox is None:
            page.screenshot(path="debug_no_textbox.png")
            raise Exception("No textbox found")

        # Step 5: Focus and type
        page.evaluate(
            """sel => {
                const el = document.querySelector(sel) || document.querySelector('[contenteditable="true"]');
                if (el) el.focus();
            }""",
            '[data-testid="tweetTextarea_0"]'
        )
        time.sleep(1)
        page.keyboard.type(text, delay=50)
        print("[tweet] typed tweet")

        # Step 6: Submit via keyboard shortcut
        textbox.click()
        time.sleep(1)
        page.keyboard.press("Control+Enter")
        print("[tweet] submitted via Ctrl+Enter")
        page.wait_for_timeout(4000)
        return True

    except Exception as e:
        page.screenshot(path="debug_error.png")
        print(f"Failed to post tweet: {e}")
        return False
