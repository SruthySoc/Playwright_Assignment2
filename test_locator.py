# # import playwright.async_api as playwright
# # import pytest
# # from dotenv import load_dotenv
# # import os
# # load_dotenv()
#
# # from Utils.config import BASE_URL
# #
# # @pytest.mark.asyncio
# # async def test_evn_(async_page):
# #     await async_page.goto(BASE_URL)
# #     print(await async_page.title())
# #
# # import pytest
# # from Utils.config import BASE_URL
# #
# # @pytest.mark.asyncio
# # async def test_evn_(async_page):
# #     await async_page.goto(BASE_URL)
#
# #tag <input, <button, <div,
# # Attribute name and attribute value
# # text- >forgot password, >
#
# # page.getByRole() to locate by explicit and implicit accessibility attributes.
# # page.getByText() to locate by text content.
# # page.getByLabel() to locate a form control by associated label's text.
# # page.getByPlaceholder() to locate an input by placeholder.
# # page.getByAltText() to locate an element, usually image, by its text alternative.
# # page.getByTitle() to locate an element by its title attribute.
# # page.getByTestId() to locate an element based on its data-testid attribute (other attributes can be configured).
#
import pytest
from playwright.async_api import expect
#
# # @pytest.mark.asyncio
# # async def test_getbyrole(async_page):
# #     await async_page.goto("https://demowebshop.tricentis.com/")
# #     reg_link = async_page.get_by_role("Link", name="Register")
# #     await expect(reg_link).to_be_visible()
# #     await reg_link.click()
# #     await expect(async_page).to_have_title("Demo Web Shop. Register")
#
#
# # @pytest.mark.asyncio
# # async def test_getbytext(async_page):
# #     await async_page.goto("https://demowebshop.tricentis.com/")
# #     excellent = async_page.get_by_text("Excellent")
# #     await expect(excellent).not_to_be_checked()
# #     await excellent.click()
# #     await expect(excellent).to_be_checked()
# #     await async_page.wait_for_timeout(5000)
# #     vb = async_page.get_by_role("radio",name="Very bad")
# #     await expect(vb).to_be_visible()
# #     await vb.click()
#
# # page.getByLabel() to locate a form control by associated label's text.
# # @pytest.mark.asyncio
# # async def test_getBylabel(async_page):
# #    await async_page.goto("https://demowebshop.tricentis.com/")
# #    reg_link =  async_page.get_by_text("Register")
# #    await expect(reg_link).to_be_visible()
# #    await reg_link.click()
# #    g = async_page.get_by_text("Female")
# #    await expect(g).to_be_visible()
# #    await g.click()
# #    fn = async_page.get_by_label("First name:")
# #    await expect(fn).to_be_visible()
# #    await fn.fill("Abc")
# #    ln = async_page.get_by_label("Last name:")
# #    await expect(ln).to_be_visible()
# #    await ln.fill("Abc")
# #    email = async_page.get_by_label("Email:")
# #    await expect(email).to_be_visible()
# #    await email.fill("abc@gmail.com")
# #    pwd = async_page.get_by_label("Password:").nth(0) # [pwd,cpwd]
# #    await expect(pwd).to_be_visible()
# #    await pwd.fill("Abc@123")
# #    cpwd = async_page.get_by_label("Confirm password:")
# #    await expect(cpwd).to_be_visible()
# #    await cpwd.fill("Abc@123")
# #    await async_page.wait_for_timeout(5000)
#
# # page.getByPlaceholder() to locate an input by placeholder.
# # @pytest.mark.asyncio
# # async def test_getByPlaceholder(async_page):
# #    await async_page.goto("https://www.amazon.in/")
# #    search_tb = async_page.get_by_placeholder("Search Amazon.in")
# #    await expect(search_tb).to_be_visible()
# #    await search_tb.fill("Books")
# #    print(search_tb.input_value())
# #    await async_page.wait_for_timeout(5000)
#
# # @pytest.mark.asyncio
# # async def test_getByPlaceholder(async_page):
# #    await async_page.goto("https://demowebshop.tricentis.com/")
# #    search_tb = async_page.get_by_placeholder("Search Amazon.in")
# #    await expect(search_tb).to_be_visible()
# #    await search_tb.fill("Books")
# #    print(search_tb.input_value())
# #    await async_page.wait_for_timeout(5000)
#
# # page.getByalt_text() to locate an image.
# @pytest.mark.asyncio
# async def test_getByalt_text(async_page):
#    await async_page.goto("https://demowebshop.tricentis.com/")
#    img = async_page.get_by_alt_text("Picture of 14.1-inch Laptop")
#    await expect(img).to_be_visible()
#    await img.click()
#    await expect(async_page).to_have_url("https://demowebshop.tricentis.com/141-inch-laptop")
#


@pytest.mark.asyncio
async def test_check_box(async_page):
    await async_page.goto("https://testautomationpractice.blogspot.com/")
    check_locator = async_page.locator("//div[@class='form-check form-check-inline']//input[@type='checkbox']/following-sibling::label")
    await expect(check_locator.first).not_to_be_checked()
    await check_locator.first.check()
    await expect(check_locator.first).to_be_checked()
    all_check_boxes = await check_locator.all_inner_texts()
    print(all_check_boxes)



@pytest.mark.asyncio
async def test_check_box_input_list(async_page):
    text_check_box = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    await async_page.goto("https://testautomationpractice.blogspot.com/")
    for i in text_check_box:
        check_locator = async_page.locator(f"//input[@id='{i.lower()}']")
        await expect(check_locator).not_to_be_checked()
        await check_locator.check()
        await expect(check_locator).to_be_checked()