import pytest
from playwright.async_api import expect

# @pytest.mark.asyncio
# async def test_check_box(async_page):
#     await async_page.goto("https://testautomationpractice.blogspot.com/")
#     check_locator = async_page.locator("//div[@class='form-check form-check-inline']//input[@type='checkbox']/following-sibling::label")
#     await expect(check_locator.first).not_to_be_checked()
#     await check_locator.first.check()
#     await expect(check_locator.first).to_be_checked()
#     all_check_boxes = await check_locator.all_inner_texts()
#     print(all_check_boxes)


#
# @pytest.mark.asyncio
# async def test_check_box_input_list(async_page):
#     text_check_box = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
#     await async_page.goto("https://testautomationpractice.blogspot.com/")
#     for i in text_check_box:
#         check_locator = async_page.locator(f"//input[@id='{i.lower()}']")
#         await expect(check_locator).not_to_be_checked()
#         await check_locator.check()
#         await expect(check_locator).to_be_checked()


#
#
# @pytest.mark.asyncio
# async def test_mul_wiind(async_page):
#     await async_page.goto("https://www.amazon.in/")
#     search_box = async_page.locator("#twotabsearchtextbox")
#     await search_box.fill("Books")
#     await search_box.press("Enter")
#     await async_page.wait_for_timeout(5000)
#     books = async_page.locator("//h2[@class='a-size-medium a-spacing-none a-color-base a-text-normal']")
#
#     # need get the wind info
#     async with async_page.expect_popup() as pop_info:
#         await books.first.click()
#
#     product_page = await pop_info.value
#     await product_page.locator("//input[@id='add-to-cart-button']").click()

# @pytest.mark.asyncio
# async def test_mul_wiind(async_page):
#     await async_page.goto("https://www.amazon.in/")
#     search_box = async_page.locator("#twotabsearchtextbox")
#     await search_box.fill("Books")
#     await search_box.press("Enter")
#     await async_page.wait_for_timeout(5000)
#     books = async_page.locator("//h2[@class='a-size-medium a-spacing-none a-color-base a-text-normal']")
#
#     # need get the wind info
#     async with async_page.expect_popup() as pop_info:
#         await books.first.click()
#
#     product_page = await pop_info.value
#
#     async with product_page.expect_popup() as product_info:
#         await product_page.locator("//input[@id='add-to-cart-button']").click()
#
#     # add_to_cart_page = await product_info.value
#     # add_to_cart_page.wait_for_load_state("domcontentloaded")
#     await product_page.locator("//input[@name='proceedToRetailCheckout']").click()

#
# import pytest
#
#
# @pytest.mark.asyncio
# async def test_mul_wiind(async_page):
#     await async_page.goto("https://www.amazon.in/")

#     search_box = async_page.locator("#twotabsearchtextbox")
#     await search_box.fill("Books")
#     await search_box.press("Enter")
#
#     # Wait for search results to load properly instead of a fixed timeout
#     books = async_page.locator("h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal")
#     await books.first.wait_for(state="visible")
#
#     # Handle the first product click (if it opens a new tab/window)
#     async with async_page.expect_popup() as pop_info:
#         await books.first.click()
#
#     product_page = await pop_info.value
#     await product_page.wait_for_load_state("domcontentloaded")
#
#     # Click 'Add to Cart' (stays on the same product page or opens a side sheet)
#     add_to_cart_btn = product_page.locator("//input[@id='add-to-cart-button']")
#     await add_to_cart_btn.click()
#
#     # Wait for the cart confirmation / side panel / elements to update
#     # If Amazon prompts a specific cart sub-page or "Proceed to Checkout" button:
#     checkout_button = product_page.locator(
#         "//input[@name='proceedToRetailCheckout' or @data-feature-id='proceed-to-checkout-action']")
#     await checkout_button.wait_for(state="visible")
#     await checkout_button.click()

# import pytest
#
# @pytest.mark.asyncio
# async def test_freams(async_page):
#     await async_page.goto("https://jqueryui.com/datepicker/")
#
#     frame = async_page.frame_locator(".demo-frame")
#
#     await frame.locator("//input[@id='datepicker']").click()
#     await frame.locator("//a[text()='14']").click()

# @pytest.mark.asyncio
# async def test_file_upload(async_page):
#     await async_page.goto("https://practice.expandtesting.com/upload#google_vignette")
#     await async_page.locator("#fileInput").set_input_files("/home/sruthy/Downloads/Flynas-Credentails.txt")
#     await async_page.locator("#fileSubmit").click()
#     msg = async_page.get_by_text("File Uploaded!")
#     await expect(msg).to_be_visible()
#
# from pathlib import Path
# @pytest.mark.asyncio
# async def test_file_upload(async_page):
#     await async_page.goto("https://demo.automationtesting.in/FileDownload.html#google_vignette")
#     # down file:-->
#     download_dir = (Path("downloads"))
#     download_dir.mkdir(parents=True, exist_ok=True)
#
#     async with async_page.expect_download() as download_dir_info:
#         await async_page.locator("(//a[text()='Download'])[1]").click()
#
#     download_ = await download_dir_info.value
#     save_path = download_dir / download_.suggested_filename
#     await download_.save_as(str(save_path))
#     print("file downloaded = " , save_path)
#     print("file is exists " , save_path.exists())
#     print("down failed" , await download_.failure())



# @pytest.mark.asyncio
# async def test_mouse_hover(async_page):
#     await async_page.goto("https://demowebshop.tricentis.com/")
#     await async_page.locator("(//a[contains(text(),'Computers')])[1]").hover()
#     await async_page.locator("(//a[contains(text(),'//h1[text()='Desktops']").click()
#     ele = async_page.locator("Desktops").first
#     await expect(ele).to_be_visible()

#
# @pytest.mark.asyncio
# async def test_du_clk(async_page):
#     await async_page.goto("https://testautomationpractice.blogspot.com/")
#     await async_page.locator("//button[text()='Copy Text']").dblclick()
#     print(await async_page.locator("#field2").input_value())
#
# import pytest
#
# @pytest.mark.asyncio
# async def test_drag_and_drop(async_page):
#     await async_page.goto("https://testautomationpractice.blogspot.com/")
#     s = async_page.locator("//div[@id = 'draggable']")
#     d = async_page.locator("//div[@id = 'droppable']")
#     await s.drag_to(d)

# @pytest.mark.asyncio
# async def test_scroll(async_page):
#     await async_page.goto("https://testautomationpractice.blogspot.com/")
#     s = async_page.locator("//div[@id = 'draggable']")
#     await s.scroll_into_view_if_needed()
#     d = async_page.locator("//div[@id = 'droppable']")
#     await s.drag_to(d)
#     await async_page.mouse.wheel(0,1000)
#     await async_page.wait_for_timeout(500)
#     await async_page.mouse.wheel(0,-1000)
#     await async_page.wait_for_timeout(500)

# @pytest.mark.asyncio
# async def test_scroll_end(async_page):
#     await async_page.goto("https://testautomationpractice.blogspot.com/")
#     await async_page.evaluate("window.scrollTo(0,document.body.scrollHeight);")
#     await async_page.wait_for_timeout(500)

#
# import pytest
# @pytest.mark.asyncio
# async def test_date_picker(async_page):
#     await async_page.goto("https://jqueryui.com/datepicker/")
#     fl = async_page.frame_locator(".demo-frame")
#     date = fl.locator("//input[@id='datepicker']")
#     await date.click()
#     day = fl.locator("//a[text()='17']")
#     await day.click()
#     #//input[@id='datepicker']
#
# @pytest.mark.asyncio
# async def test_date_picker(async_page):
#     um = "January"
#     uy = "2027"
#     ud = "22"
#
#     await async_page.goto("https://jqueryui.com/datepicker/")
#     fl = async_page.frame_locator(".demo-frame")
#     date = fl.locator("//input[@id='datepicker']")
#     await date.click()
#
#     cm = await fl.locator(".ui-datepicker-month").inner_text()
#     cy = await fl.locator(".ui-datepicker-year").inner_text()
#     print(cm)
#     print(cy)
#     while (True):
#         if (uy == cy and um == cm):
#             await fl.locator(f"//a[text()='{ud}']").click()
#             break
#         await fl.locator("//span[text()='Next']").click()
#         cm = await fl.locator(".ui-datepicker-month").inner_text()
#         cy = await fl.locator(".ui-datepicker-year").inner_text()

#
# @pytest.mark.asyncio
# async def test_range_slider(async_page):
#     await async_page.goto("https://jqueryui.com/resources/demos/slider/range.html?utm_source")
#     min = 100
#     max = 400
#
#     slider = async_page.locator("//div[@id='slider-range']/span")
#     await slider.nth(0).focus()
#     await slider.nth(0).press("Home")
#
#     for i in range(min):
#         await slider.nth(0).press("ArrowRight")
#
#     await slider.nth(1).focus()
#     await slider.nth(1).press("End")
#     for i in range(max):
#         await slider.nth(0).press("ArrowLeft")

#
@pytest.mark.asyncio
async def test_end_to_end(async_page):
    await async_page.goto("https://demowebshop.tricentis.com/")

    # =============================================================================
    # ====================== Reg
    # =================================================================================
    await async_page.locator("//a[text()='Register']").click()
    await async_page.get_by_label("First name:").fill("abc")
    await async_page.get_by_label("Last name:").fill("abc")
    await async_page.get_by_label("Email:").fill("abcd1234@gmail.com")
    await async_page.get_by_label("Password:").nth(0).fill("abc@123")
    await async_page.get_by_label("Confirm password:").fill("abc@123")
    await async_page.locator("#register-button").click()

    try:
        await async_page.get_by_text("Log out").is_visible()

    except Exception:
          print(await async_page.locator("//span[@class='field-validation-error']").all_text_contents())

    # =============================================================================
    # ====================== login
    # =================================================================================
    await async_page.get_by_text("Log in").click()
    await async_page.get_by_label("Email:").fill("abcdefg333@gmail.com")
    await async_page.get_by_label("Password:").fill("abc@123")
    await async_page.locator("//input[@value='Log in']").click()
    try:
        await async_page.get_by_text("Log out").is_visible()

    except Exception:
        print(await async_page.locator("//span[@class='field-validation-error']").all_text_contents())

