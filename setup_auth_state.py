
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

APP_URL = "https://your-authorized-test-app.example/"
AUTH_INDICATOR = '[data-testid="account-menu"]'
STATE_FILE = Path(__file__).parent / ".auth" / "storage_state.json"


async def main():
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(APP_URL)

            print("Complete authorized sign-in if required.")
            print("Do not enter real personal or payment data.")

            # Complete the approved sign-in manually.
            # Resume the script after sign-in.
            await page.pause()

            # Save state only after authentication is verified.
            await page.locator(AUTH_INDICATOR).wait_for(
                state="visible",
                timeout=10000
            )

            await context.storage_state(path=str(STATE_FILE))
            print(f"Browser state saved to: {STATE_FILE}")

        finally:
            await context.close()
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
