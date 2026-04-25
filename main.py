import asyncio
import time
from datetime import datetime
from src.engine import run_vote_logic
from src.utils import log_progress, load_proxies
from playwright.async_api import async_playwright

# --- CONFIGURATION ---
URL = "https://strawpoll.com/wAg3QdLVdy8"
CANDIDATE = "Hon. John Mutunga"
VOTES_PER_SECOND = 2
DURATION_SECONDS = 3600 # 1 Hour test

async def main():
    success_count = 0
    fail_count = 0
    start_time = datetime.now()
    end_time = time.time() + 3600 

    async with async_playwright() as p:
        # headless=False is better for 'No Proxy' testing so you can see if you get blocked
        browser = await p.chromium.launch(headless=False) 
        
        while time.time() < end_time:
            iteration_start = time.time()
            
        
            # (Running 2 per second on one IP will get you banned in seconds)
            success = await run_vote_logic(browser, None, URL, CANDIDATE)
            
            if success: success_count += 1
            else: fail_count += 1
            
            log_progress(success_count, fail_count, start_time)

            # Wait a bit longer between votes to try and avoid detection
            await asyncio.sleep(1.0) 

        await browser.close()