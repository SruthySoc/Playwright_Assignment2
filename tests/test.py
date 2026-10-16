# def test_for_open_website(page):
#     page.goto("https://b2ebeta.akbarcorporate.com/login")

# from playwright.sync_api import sync_playwright, expect
#
# def test_async_sync_exp3(page):
#     page.goto("https://www.facebook.com/")
#     print(page.title())
#     expect(page).to_have_title("My Facebook")
#     page.goto("https://www.amazon.in/")
#     expect(page).to_have_url("https://www.amazon.in/")
#     page.go_back()
#     page.go_forward()
#     page.reload()

from playwright.sync_api import sync_playwright, expect
import pytest

@pytest.mark.asyncio
 async def test_for_async(async_page):
