import asyncio
import random
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def run_vote_logic(browser, proxy, target_url, candidate_name):
    # 1. Setup Context with high-resolution fingerprinting
    context = await browser.new_context(
        proxy={"server": proxy} if proxy else None,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    )
    page = await context.new_page()
    await stealth_async(page)

    # 2. Optimization: Block images and media to speed up voting
    await page.route("*/.{png,jpg,jpeg,svg,mp4,css}", lambda route: route.abort())

    try:
        # 3. Go to URL - Using 'commit' instead of 'networkidle' for speed
        await page.goto(target_url, wait_until="commit", timeout=20000)
        
        # 4. Wait for the candidate text to appear
        # Strawpoll usually renders options in labels or spans
        selector = f"text={candidate_name}"
        await page.wait_for_selector(selector, timeout=5000)
        
        # 5. Execute Vote
        await page.click(selector)
        
        # Target the vote button by ID or class (Strawpoll usually uses 'button-vote')
        await page.click("button.button-vote, #vote-button, .vote-button")
        
        # 6. Optional: Verify success message
        # await page.wait_for_selector(".success-message", timeout=2000)
        return True
    except Exception as e:
        return False
    finally:
        await context.close()