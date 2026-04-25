import asyncio
import random
from playwright_stealth import stealth_async

async def run_vote_logic(browser, target_url, candidate_name):
    # 1. Create a completely isolated incognito context (No Cookies/Cache)
    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0.0.0 Safari/537.36",
        # Force a fresh 'Identity' in the headers
        extra_http_headers={
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://google.com/",
            "DNT": "1" # Do Not Track header
        }
    )
    
    page = await context.new_page()
    await stealth_async(page)

    try:
        # 2. Fast Navigation
        await page.goto(target_url, wait_until="domcontentloaded", timeout=15000)
        
        # 3. Dynamic Selector Logic
        # We find the candidate by searching for the text within the poll options
        candidate_selector = f"text={candidate_name}"
        await page.wait_for_selector(candidate_selector, timeout=5000)
        await page.click(candidate_selector)
        
        # 4. Submit Vote
        # Strawpoll uses different IDs; this selector targets common button patterns
        vote_btn = page.locator('button:has-text("Vote"), .button-vote, #vote-button')
        await vote_btn.click()
        
        # Give the server a moment to register the vote before closing
        await asyncio.sleep(1)
        return True
    except Exception:
        return False
    finally:
        # Critical: Close the context to wipe all session data
        await context.close()