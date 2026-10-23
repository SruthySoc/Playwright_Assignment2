
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_checkout_form_persistence(async_page):
    # Open the local mock form
    await async_page.goto("file:///absolute/path/to/mock_checkout.html")

    name = async_page.locator("#name")
    email = async_page.locator("#email")
    address = async_page.locator("#address")
    city = async_page.locator("#city")

    # Verify initial test data
    await expect(name).to_have_value("Test User")
    await expect(email).to_have_value("test@example.com")

    print("Step 1 fields are populated")

    # Move forward
    await async_page.get_by_role(
        "button", name="Continue"
    ).click()

    await expect(async_page.locator("#step2")).to_be_visible()

    # Enter safe, synthetic delivery data
    await address.fill("456 Demo Avenue")
    await city.fill("Sample City")

    await expect(address).to_have_value("456 Demo Avenue")
    await expect(city).to_have_value("Sample City")

    print("Step 2 fields are populated")

    # Navigate backward
    await async_page.get_by_role("button", name="Back").click()

    await expect(async_page.locator("#step1")).to_be_visible()

    # Verify Step 1 values remain populated
    await expect(name).to_have_value("Test User")
    await expect(email).to_have_value("test@example.com")

    print("Step 1 values persisted after navigating back")

    # Navigate forward again
    await async_page.get_by_role(
        "button", name="Continue"
    ).click()

    await expect(async_page.locator("#step2")).to_be_visible()

    # Verify Step 2 values remain populated
    await expect(address).to_have_value("456 Demo Avenue")
    await expect(city).to_have_value("Sample City")

    print("Step 2 values persisted after navigating forward")

    # Complete the demo only; no order is submitted
    await async_page.get_by_role(
        "button", name="Finish Demo"
    ).click()

    await expect(async_page.locator("#message")).to_have_text(
        "Demo completed. No order was submitted."
    )
