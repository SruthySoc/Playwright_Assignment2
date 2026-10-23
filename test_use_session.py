import pytest
from playwright.async_api import async_playwright
@pytest.mark.asyncio
async def test_use_session(async_page):
    await async_page.goto("https://demowebshop.tricentis.com/")
    await async_page.wait_for_timeout(5000)