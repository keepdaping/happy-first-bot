from datetime import datetime
from .auth import login
from .tweet import post_tweet
from .config import FORCE_RUN


def main():
    if not FORCE_RUN and datetime.now().day != 1:
        print("Not the 1st of the month. Exiting.")
        return

    playwright = None
    browser = None
    try:
        playwright, browser, page = login()
        success = post_tweet(page, "happy 1st.")
        print("Tweet posted." if success else "Failed to post tweet.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if browser:
            browser.close()
        if playwright:
            playwright.stop()


if __name__ == "__main__":
    main()
