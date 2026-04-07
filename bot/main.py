from datetime import datetime
from auth import login
from tweet import post_tweet


def main():
    if datetime.now().day != 7:
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
