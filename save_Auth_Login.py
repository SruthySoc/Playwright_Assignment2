# login :--> application :-->login
# login :-->complet session i am store session.json
# order :--> add to cart  login
# fix data :--> .env  :-->
import os
from _pytest._py import path
from dotenv import load_dotenv
import pytest
from playwright.async_api import expect
from playwright.async_api import async_playwright
from pathlib import Path

AUTH_DIR = Path(".auth")
AUTH_DIR.mkdir(parents=True, exist_ok=True)
AUTH_FILE = AUTH_DIR / "loginsession.json"

load_dotenv()
@pytest.mark.asyncio
async def test_mul_data():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        async_page = await browser.new_page()
        url = os.getenv("BASE_URL")
        email = os.getenv("WEBSHOP_USER")
        pwd = os.getenv("WEBSHOP_PASS")
        await  async_page.goto(url)
        await async_page.get_by_text("Log in").click()
        await async_page.locator("#Email").fill(email)
        await async_page.locator("#Password").fill(pwd)
        await async_page.locator("//input[@value='Log in']").click()
        await expect(async_page.get_by_text("Log out")).to_be_visible()
        await context.storage_state(path=str(AUTH_FILE))
        print("login session created " , AUTH_FILE)
        await browser.close()