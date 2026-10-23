# # type :-->Random data
# # fp :--> Ben :-> 5600104,564001,
# # type :static data:--> acc_num
# import string
# import random
#
#
# def gen_random_data_email():
#     user_name = ''.join(random.choices(string.ascii_lowercase+string.digits,k=10))
#     return f"{user_name}.@gmail.com"
# def gen_random_data_ph():
#     return "".join(random.choices(string.digits,k = 10))
# def gen_randon_user_name():
#     return "".join(random.choices(string.ascii_letters,k = 10))
# def gen_random_pwd():
#     return "".join(random.choices(string.ascii_uppercase+string.ascii_lowercase+string.digits,k = 10))
#
#
# def reg_data():
#     l = {"user_name" :gen_randon_user_name(),"email" : gen_random_data_email(),"pwd" : gen_random_pwd()}
#     print(l)
#     return l
# print(reg_data())


# type :-->Random data
# fp :--> Ben :-> 5600104,564001,
# # type :static data:--> acc_num
# import string
# import random
#
# from playwright.async_api import expect
#
#
# def gen_random_data_email():
#     user_name = ''.join(random.choices(string.ascii_lowercase+string.digits,k=10))
#     return f"{user_name}.@gmail.com"
# def gen_random_data_ph():
#     return "".join(random.choices(string.digits,k = 10))
# def gen_randon_user_name():
#     return "".join(random.choices(string.ascii_letters,k = 10))
# def gen_random_pwd():
#     return "".join(random.choices(string.ascii_uppercase+string.ascii_lowercase+string.digits,k = 10))
#
#
# def reg_data():
#     l = {"user_name" :gen_randon_user_name(),"email" : gen_random_data_email(),"pwd" : gen_random_pwd()}
#     return l
# print(reg_data())
#
#
#
#
# import pytest
# @pytest.mark.asyncio
# async def test_mul_data(async_page):
#     data = reg_data()
#     await async_page.goto("https://demowebshop.tricentis.com/")
#     await async_page.get_by_text("Register").click()
#     ele = async_page.get_by_text("Register")
#     expect(ele).to_be_visible()
#     fn = async_page.locator("#FirstName")
#     await fn.fill(data["user_name"])
#     ln = async_page.locator("#LastName")
#     await ln.fill("l")
#     email = async_page.locator("#Email")
#     await email.fill(data["email"])
#     pwd = async_page.locator("#Password").nth(0)
#     await pwd.fill(data["pwd"])
#     cpwd = async_page.locator("#ConfirmPassword")
#     await cpwd.fill(data["pwd"])
#     print(f"first name is {await fn.input_value()} \n last name is { await ln.input_value()} \n email id is {await email.input_value()} \n pwd is {await pwd.input_value() } \n cpwd is {await cpwd.input_value()}")
#     await async_page.locator("#register-button").click()
# import string
# import random
# from playwright.async_api import expect
# def gen_random_data_email():
#     user_name = ''.join(random.choices(string.ascii_lowercase+string.digits,k=10))
#     return f"{user_name}@gmail.com"
# def gen_random_data_ph():
#     return "".join(random.choices(string.digits,k = 10))
# def gen_randon_user_name():
#     return "".join(random.choices(string.ascii_letters,k = 10))
# def gen_random_pwd():
#     return "".join(random.choices(string.ascii_uppercase+string.ascii_lowercase+string.digits,k = 10))
#
#
# def reg_data():
#     l = {"user_name" :gen_randon_user_name(),"email" : gen_random_data_email(),"pwd" : gen_random_pwd()}
#     return l
# print(reg_data())
#
#
#
#
# import pytest
# @pytest.mark.asyncio
# async def test_mul_data(async_page):
#     data = reg_data()
#     await async_page.goto("https://demowebshop.tricentis.com/")
#     await async_page.get_by_text("Register").click()
#     ele = async_page.get_by_text("Register")
#     expect(ele).to_be_visible()
#     fn = async_page.locator("#FirstName")
#     await fn.fill(data["user_name"])
#     ln = async_page.locator("#LastName")
#     await ln.fill("l")
#     email = async_page.locator("#Email")
#     await email.fill(data["email"])
#     pwd = async_page.locator("#Password").nth(0)
#     await pwd.fill(data["pwd"])
#     cpwd = async_page.locator("#ConfirmPassword")
#     await cpwd.fill(data["pwd"])
#     print(f"first name is {await fn.input_value()} \n last name is { await ln.input_value()} \n email id is {await email.input_value()} \n pwd is {await pwd.input_value() } \n cpwd is {await cpwd.input_value()}")
#     await async_page.locator("#register-button").click()
#     await async_page.wait_for_timeout(50000)
#     await expect(async_page.locator("//div[@class='result']")).to_contain_text("Your registration completed")
#     await expect(async_page.get_by_text(data["email"])).to_be_visible()
#

import pytest
from playwright.async_api import async_playwright
@pytest.mark.asyncio
async def test_use_session():
    async  with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=".auth/loginsession.json")
        page = await context.new_page()
        await page.goto("https://demowebshop.tricentis.com/")
        await page.wait_for_timeout(5000)
@pytest.mark.asyncio
async def test_mul_data():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        async_page = await context.new_page()
        url = os.getenv("BASE_URL")
        email = os.getenv("WEBSHOP_USER")
        pwd = os.getenv("WEBSHOP_PASS")
        await  async_page.goto(url)
        await async_page.get_by_text("Log in").click()
        await async_page.locator("#Email").fill(email)
        await async_page.locator("#Password").fill(pwd)
        await async_page.locator("//input[@value='Log in']").click()
        try:
            await expect(async_page.get_by_text("Log out")).to_be_visible()
            await context.storage_state(path=str(AUTH_FILE))
            print("login session created " , AUTH_FILE)
        except Exception as e:
            print("login session not created")
        await browser.close()

