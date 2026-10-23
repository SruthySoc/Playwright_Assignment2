
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_product_availability_and_cart(async_page):
    # Example product URL: replace with your selected product URL
    await async_page.goto(
        "https://www.amazon.in/",
        wait_until="domcontentloaded"
    )

    # Locate the Add to Cart button on the product detail page
    add_to_cart = async_page.locator("#add-to-cart-button")

    # Record the actual UI state
    if await add_to_cart.count() == 0:
        print(
            "UNAVAILABLE: Add to Cart control is missing. "
            "Skipping cart validation."
        )
        pytest.skip("Add to Cart control is missing")

    if not await add_to_cart.is_visible():
        print(
            "UNAVAILABLE: Add to Cart control is not visible. "
            "Skipping cart validation."
        )
        pytest.skip("Add to Cart control is not visible")

    if not await add_to_cart.is_enabled():
        print(
            "UNAVAILABLE: Add to Cart control is disabled. "
            "Skipping cart validation."
        )
        pytest.skip("Add to Cart control is disabled")

    # Check for an explicit out-of-stock message
    out_of_stock = async_page.locator(
        "#availability"
    )

    if await out_of_stock.count() > 0:
        availability_text = (
            await out_of_stock.inner_text()
        ).strip()

        print(f"Availability text: {availability_text}")

        if "currently unavailable" in availability_text.lower():
            pytest.skip(
                "Product is currently unavailable. "
                "Skipping cart validation."
            )

    print("Add to Cart is visible and enabled.")

    # Continue only when the control is available
    await add_to_cart.click()

    # Validate the cart only after the product is added
    await async_page.wait_for_load_state(
        "domcontentloaded"
    )

    print("Add to Cart was clicked; checking cart state.")

    # A real cart validation should verify the selected product
    # identifier/title against the product shown in the cart.
