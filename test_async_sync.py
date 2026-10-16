# import asyncio
#
from playwright.sync_api import sync_playwright, expect
#
# def test_async_sync_exp1():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         user_context = browser.new_context()
#         page = user_context.new_page()
#         page.goto("https://www.facebook.com/")
#         print(page.title())
#         expect(page).to_have_title("Facebook")
#
# async def test_async_sync_exp2():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         user_context = await browser.new_context()
#         page = await user_context.new_page()
#         await page.goto("https://www.facebook.com/")
#         print(page.title())
#         await expect(page).to_have_title("Facebook")
#
# asyncio.run(test_async_sync_exp2())

# def test_async_sync_exp3(page):
#     page.goto("https://www.facebook.com/")
#     print(page.title())
#     expect(page).to_have_title("Facebook")

# pytest-twisted





