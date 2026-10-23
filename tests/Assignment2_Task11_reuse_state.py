
from pathlib import Path

import pytest
from playwright.async_api import async_playwright

APP_URL = "https://your-authorized-test-app.example/"
AUTH_INDICATOR = '[data-testid="account-menu"]'
LOGIN_PATHS = ("/login", "/signin")

STATE_FILE = (
    Path(__file__).resolve().parents[1]
    / ".auth"
    / "storage_state.json"
)


@pytest.mark.asyncio
async def test_reuse_saved_authentication():
    if not STATE_FILE.is_file():
        pytest.fail(
            f"Missing state file: {STATE_FILE}. "
            "Run setup_auth_state.py first."
        )

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        try:
            context = await browser.new_context(
                storage_state=str(STATE_FILE)
            )
            page = await context.new_page()

            try:
                await page.goto(
                    APP_URL,
                    wait_until="domcontentloaded"
                )

                # Detect a redirect to sign-in.
                if any(path in page.url.lower()
                       for path in LOGIN_PATHS):
                    pytest.fail(
                        "Saved session expired. "
                        "Authorized re-authentication is needed."
                    )

                # Verify that the authenticated indicator appears.
                try:
                    await page.locator(
                        AUTH_INDICATOR
                    ).wait_for(
                        state="visible",
                        timeout=10000
                    )
                except Exception:
                    pytest.fail(
                        "Authenticated state not confirmed. "
                        "The session may have expired, or the "
                        "account indicator selector may be incorrect."
                    )

                print(
                    "PASS: Authenticated state reused in "
                    "a new browser context."
                )

            finally:
                await context.close()

        finally:
            await browser.close()


def require_state_file(path):
    if not path.is_file():
        raise FileNotFoundError(
            f"Authentication state missing: {path}. "
            "Run setup_auth_state.py first."
        )


def test_missing_state_file_handled():
    missing_file = STATE_FILE.parent / "missing_state.json"

    with pytest.raises(
        FileNotFoundError,
        match="Authentication state missing"
    ):
        require_state_file(missing_file)

    print("PASS: Missing state file reported clearly.")
