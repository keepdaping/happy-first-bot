from playwright.sync_api import Page
import time


def post_tweet(page: Page, text: str) -> bool:
    try:
        # Step 1: Ensure on home page
        if "x.com/home" not in page.url:
            page.goto("https://x.com/home", wait_until="domcontentloaded")
        page.wait_for_timeout(6000)

        print("[tweet] on home page:", page.url)

        # Debug: page info
        title = page.title()
        print(f"[tweet] page title: {title}")
        body_text = page.locator("body").inner_text()[:500]
        print(f"[tweet] body text start: {body_text}")

        # Step 2: The compose textbox should be visible on home page
        # No need to click post button, as compose is inline

        # Step 3: Find textbox
        textbox = None

        # Debug: find all possible text inputs
        all_inputs = page.locator('input, textarea, [contenteditable], [role="textbox"]').all()
        print(f"[tweet] found {len(all_inputs)} possible inputs")
        for i, inp in enumerate(all_inputs[:10]):  # limit to 10
            try:
                tag = inp.evaluate("el => el.tagName")
                testid = inp.get_attribute("data-testid") or ""
                role = inp.get_attribute("role") or ""
                contenteditable = inp.get_attribute("contenteditable") or ""
                print(f"[tweet] input {i}: {tag} data-testid={testid} role={role} contenteditable={contenteditable}")
            except:
                pass

        # Debug: find elements with "What’s happening?"
        whats_happening = page.locator('text="What’s happening?"').all()
        print(f"[tweet] found {len(whats_happening)} 'What’s happening?' elements")
        for i, el in enumerate(whats_happening[:5]):
            try:
                tag = el.evaluate("el => el.tagName")
                parent = el.locator("..")
                parent_tag = parent.evaluate("el => el.tagName")
                print(f"[tweet] whats {i}: {tag} parent {parent_tag}")
            except:
                pass

        for sel in [
            '[data-testid="tweetTextarea_0"]',
            '[data-testid="tweetTextarea_1"]',
            '[data-testid="Tweet-User-Text-Input"]',
            'div[role="textbox"]',
            '[role="textbox"]',
            '[contenteditable="true"]',
            'textarea',
            '.DraftEditor-editorContainer',
            '.public-DraftEditor-content',
        ]:
            try:
                tb = page.locator(sel).first
                tb.wait_for(state="visible", timeout=10000)
                textbox = tb
                print(f"[tweet] textbox found: {sel}")
                break
            except Exception:
                continue

        if textbox is None:
            page.screenshot(path="debug_no_textbox.png")
            raise Exception("Textbox not found on home page")

        # Step 4: Type tweet
        textbox.click()
        page.wait_for_timeout(1000)
        textbox.fill("")
        textbox.type(text, delay=50)

        print("[tweet] typed tweet")

        # Step 5: Submit
        submit_button = page.locator('[data-testid="tweetButtonInline"]').first
        submit_button.wait_for(state="visible", timeout=5000)
        submit_button.click()

        page.wait_for_timeout(5000)

        return True

    except Exception as e:
        page.screenshot(path="debug_error.png")
        print(f"Failed to post tweet: {e}")
        return False
