import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Launching the browser (headless=False so you can see it)
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://playwright.dev")
        print(f"Page Title: {await page.title()}")
        await browser.close()

asyncio.run(run())