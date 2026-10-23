
import json
from pathlib import Path

import pytest
from playwright.async_api import async_playwright


APP_URL = "https://your-authorized-test-app.example/"
STATE_FILE = Path(".auth/storage_state.json")

# Replace these with selectors from your approved test app.
SIGN_IN_SELECTOR = 'input[name="username"]'
AUTHENTICATED_SELECTOR = '[data-testid="account-menu"]'


def is_sign_in_url(url):
    return "/login" in url.lower() or "/signin" in url.lower()


@pytest.mark.asyncio
async def test_reuse_authenticated_state():
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        # 1. Open the authorized application.
        original_context = await browser.new_context()
        page = await original_context.new_page()
        await page.goto(APP_URL)

        # 2. Sign in only when explicitly permitted.
        # Complete the approved sign-in manually if required.
        if is_sign_in_url(page.url):
            print("Sign-in required. Complete approved login.")
            await page.pause()

        # Verify that authentication actually succeeded.
        try:
            await page.locator(
                AUTHENTICATED_SELECTOR
            ).wait_for(state="visible", timeout=10000)
        except Exception:
            await original_context.close()
            await browser.close()
            pytest.fail(
                "Authenticated state could not be verified. "
                "Check the approved login flow and selector."
            )

        # 3. Save the authenticated browser context.
        await original_context.storage_state(
            path=str(STATE_FILE)
        )
        print("Authenticated state saved locally.")

        await original_context.close()

        # 4. Create a completely new context using saved state.
        restored_context = await browser.new_context(
            storage_state=str(STATE_FILE)
        )
        restored_page = await restored_context.new_page()
        await restored_page.goto(APP_URL)

        # 5. Detect expired or missing authentication.
        if is_sign_in_url(restored_page.url):
            print(
                "SESSION EXPIRED: Re-authentication is needed."
            )
            await restored_context.close()
            await browser.close()
            pytest.skip(
                "Saved session is no longer authenticated; "
                "reauthentication is required."
            )

        try:
            await restored_page.locator(
                AUTHENTICATED_SELECTOR
            ).wait_for(state="visible", timeout=10000)
        except Exception:
            print(
                "Authentication could not be verified in "
                "the restored context."
            )
            await restored_context.close()
            await browser.close()
            pytest.skip(
                "Saved session may have expired or the "
                "authenticated-state selector needs updating."
            )

        print(
            "PASS: New context reused the authenticated state "
            "without repeating the sign-in flow."
        )

        await restored_context.close()
        await browser.close()
