# Happy First Bot

A Twitter (X) automation bot that posts "happy 1st." on the first day of every month.

## Project Overview

| Aspect | Details |
|--------|---------|
| **Purpose** | Automated tweet posting on the 1st of each month |
| **Target** | Twitter/X platform |
| **Automation** | Playwright (Chromium browser) |
| **Language** | Python |

## Project Structure

```
happy-first-bot/
├── requirements.txt    # Python dependencies
├── session.json        # Twitter session cookies (user-provided)
└── bot/
    ├── __init__.py     # Package marker (empty)
    ├── auth.py         # Login via cookies + Playwright
    ├── config.py       # Configuration settings
    ├── main.py         # Entry point - runs on 1st of month
    └── tweet.py        # Tweet posting logic
```

## Dependencies

- **playwright** - Browser automation framework

Install via: `pip install -r requirements.txt`

## How It Works

### 1. Authentication ([auth.py](bot/auth.py))
- Loads cookies from `session.json` (must be provided by user)
- Supports two formats:
  - Bare list: `[{ "name": "...", "value": "...", ... }, ...]`
  - Object: `{ "cookies": [{ "name": "...", "value": "...", ... }, ...] }`
- Launches Chromium browser (headless configurable)
- Adds cookies to browser context
- Navigates to X.com home page

### 2. Configuration ([config.py](bot/config.py))
```python
HEADLESS_MODE = False  # Set True to run browser in headless mode
```

### 3. Main Entry ([main.py](bot/main.py))
- Checks if current date is the 1st of the month
- If not 1st: exits silently
- If 1st: runs login + posts tweet "happy 1st."
- Handles cleanup (closes browser, stops playwright)

### 4. Tweet Posting ([tweet.py](bot/tweet.py))
- Navigates to X.com home if not already there
- Locates the tweet textbox using multiple selector strategies:
  - `data-testid="tweetTextarea_0"`
  - `data-testid="tweetTextarea_1"`
  - `div[role="textbox"]`
  - `textarea`
  - And more fallbacks
- Types the tweet text with realistic delay
- Clicks the submit button (`data-testid="tweetButtonInline"`)
- Takes screenshots on failure for debugging

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Get Twitter Session Cookies
1. Log into Twitter in your browser
2. Open DevTools (F12) → Application tab → Cookies
3. Export cookies as JSON
4. Save as `session.json` in project root

### 3. Configure
Edit [config.py](bot/config.py) to set `HEADLESS_MODE = True` for production

### 4. Run
```bash
python -m bot.main
```

## Key Features

- ✅ Runs only on the 1st of the month
- ✅ Uses existing session (no credentials needed)
- ✅ Multiple fallback selectors for tweet box
- ✅ Debug screenshots on failure
- ✅ Proper browser cleanup

## Potential Improvements

- Error handling for missing session.json
- Logging to file instead of stdout
- Retry mechanism for failed posts
- Environment variable configuration
- Support for custom tweet messages
- CI/CD scheduling (GitHub Actions, etc.)