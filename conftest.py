import pytest
from playwright.async_api import async_playwright
import pytest_asyncio

@pytest_asyncio.fixture()
async def async_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        yield page
        await browser.close()

@pytest_asyncio.fixture()
async def chromium_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        yield page

@pytest_asyncio.fixture()
async def firefox_page():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        yield page

@pytest.mark.asyncio
async def test_scroll(async_page):
    await async_page.goto("https://testautomationpractice.blogspot.com/")
    s = async_page.locator("//div[@id = 'draggable']")
    await s.scroll_into_view_if_needed()
    d = async_page.locator("//div[@id = 'droppable']")
    await s.drag_to(d)

@pytest_asyncio.fixture
async def async_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) # chromebrowser
        context = await browser.new_context(storage_state=".auth/loginsession.json")
        page = await context.new_page() # page
        yield  page
        await browser.close()

@pytest.fixture
def approved_product_api():
    return {
        "source_endpoint": "mock://trainer-product-api/products/123",
        "product": {
            "id": "123",
            "title": "Logitech Wireless Mouse",
        },
    }