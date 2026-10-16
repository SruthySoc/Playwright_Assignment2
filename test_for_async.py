
# from playwright.async_api import async_playwright
# import pytest
# @pytest.mark.asyncio
# async def test_for_async(async_page):
#     await async_page.goto("https://www.amazon.com/")

#
# from playwright.async_api import async_playwright
# import pytest
#
# @pytest.mark.asyncio
# async def test_diff_browser():
#     async with async_playwright() as p:
#         chrome_browser = await p.chromium.launch(headless=True)
#         user_context = await chrome_browser.new_context()
#         page = await user_context.new_page()
#         await page.goto("www.amazon.com")
#
#         admin_context = await chrome_browser.new_context()
#         page = await admin_context.new_page()
#         await page.goto("www.amazon.com")


# from playwright.async_api import async_playwright
# import pytest
#
# @pytest.mark.asyncio
# async def test_diff_browser():
#
#     async with async_playwright() as p:
#
#         chrome_browser = await p.chromium.launch(headless=False)
#         user_context = await chrome_browser.new_context()
#         page = await user_context.new_page()
#         await page.goto("http://google.com")
#
#         admin_context = await chrome_browser.new_context()
#         page = await admin_context.new_page()
#         await page.goto("https://www.amazon.in/")
#
#         firefox_browser = await p.firefox.launch(headless=False)
#         user_context = await firefox_browser.new_context()
#         page = await user_context.new_page()
#         await page.goto("http://google.com")
#
#         admin_context = await firefox_browser.new_context()
#         page = await admin_context.new_page()
#         await page.goto("https://www.amazon.in/")

#####################################################

# from playwright.async_api import async_playwright
# import pytest
# @pytest.mark.asyncio
# async def test_diff_browser():
#     async with async_playwright() as p:
#         chrome_browser = await p.chromium.launch(headless=False)
#
#         user_context = await chrome_browser.new_context()
#         user_page = await user_context.new_page()
#         await user_page.goto("https://www.amazon.com/")
#
#         admin_context = await chrome_browser.new_context()
#         admin_page = await admin_context.new_page()
#         await admin_page.goto("https://www.amazon.com/")

