import asyncio
import time
from datetime import datetime
from src.engine import run_vote_logic
from playwright.async_api import async_playwright

# --- HARDCODED CONFIGURATION FOR INTERNAL AUDIT ---
TARGET_URL = "https://strawpoll.com/wAg3QdLVdy8"
CANDIDATE_NAME = "Hon. John Mutunga"
VOTES_PER_SECOND = 2
TEST_DURATION_SECONDS = 3600 

async def main():
    success_count = 0
    fail_count = 0
    start_time = datetime.now()
    end_time = time.time() + TEST_DURATION_SECONDS

    print(f"--- INTERNAL AUDIT STARTED: {start_time.strftime('%H:%M:%S')} ---")

    async with async_playwright() as p:
        # headless=False to monitor the first few votes visually
        browser = await p.chromium.launch(headless=False) 
        
        while time.time() < end_time:
            loop_start = time.time()
            
            # Executing votes in parallel batches
            tasks = [run_vote_logic(browser, TARGET_URL, CANDIDATE_NAME) for _ in range(VOTES_PER_SECOND)]
            results = await asyncio.gather(*tasks)
            
            for res in results:
                if res: success_count += 1
                else: fail_count += 1
            
            # Progress Logging
            elapsed = datetime.now() - start_time
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Success: {success_count} | Fail: {fail_count}")

            # Throttling to maintain the 2/sec rate
            wait = max(0, 1.0 - (time.time() - loop_start))
            await asyncio.sleep(wait)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())