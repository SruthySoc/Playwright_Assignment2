# from playwright.async_api import async_playwright
import pytest

@pytest.mark.asyncio
async def test_chrome_browser(chromium_page):
    await chromium_page.goto("https://www.google.com/")

@pytest.mark.asyncio
async def test_firefox_browser(firefox_page):
    await firefox_page.goto("https://www.google.com/")