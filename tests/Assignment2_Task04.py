
import re
import pytest
from playwright.async_api import async_playwright, expect


# Replace with the keyword provided by your trainer
SEARCH_KEYWORD = "wireless mouse"

# Set this to a distinctive phrase from the expected product title
REQUIRED_PRODUCT_NAME = "wireless mouse"


def normalize(text):
    return " ".join(text.split()).casefold()


@pytest.mark.asyncio
async def test_amazon_cart_and_safe_checkout():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # 1. Open Amazon India
            await page.goto(
                "https://www.amazon.in/",
                wait_until="domcontentloaded",
                timeout=60000
            )

            search_box = page.locator("#twotabsearchtextbox")
            await expect(search_box).to_be_visible(timeout=20000)

            # 2. Search for the product
            await search_box.fill(SEARCH_KEYWORD)
            await search_box.press("Enter")

            product_cards = page.locator(
                'div[data-component-type="s-search-result"]'
            )

            await expect(product_cards.first).to_be_visible(
                timeout=30000
            )

            # 3. Find a product by visible title, not fixed position
            selected_card = None
            selected_title = None

            for index in range(await product_cards.count()):
                card = product_cards.nth(index)
                title_locator = card.locator("h2").first

                if await title_locator.count() == 0:
                    continue

                title = (await title_locator.inner_text()).strip()

                if (
                    REQUIRED_PRODUCT_NAME.casefold()
                    in title.casefold()
                ):
                    link = card.locator("h2 a").first

                    if await link.get_attribute("href"):
                        selected_card = card
                        selected_title = title
                        break

            assert selected_card is not None, (
                f"PRODUCT NOT FOUND: No result matched "
                f"'{REQUIRED_PRODUCT_NAME}' for "
                f"'{SEARCH_KEYWORD}'."
            )

            print(f"Selected product: {selected_title}")

            # 4. Open the selected product detail page
            await selected_card.locator("h2 a").first.click()

            title_locator = page.locator("#productTitle")
            await expect(title_locator).to_be_visible(timeout=30000)

            detail_title = (await title_locator.inner_text()).strip()
            print(f"Detail page title: {detail_title}")

            assert normalize(selected_title) == normalize(detail_title), (
                "PRODUCT TITLE MISMATCH: Search result and detail "
                "page titles are different."
            )

            print("PASS: Product title validated")

            # 5. Check Add to Cart availability
            add_to_cart = page.locator("#add-to-cart-button")

            if await add_to_cart.count() == 0:
                pytest.fail(
                    "ADD TO CART UNAVAILABLE: The product page does "
                    "not contain the expected Add to Cart control."
                )

            if not await add_to_cart.is_visible():
                pytest.fail(
                    "ADD TO CART UNAVAILABLE: The control is not visible."
                )

            if not await add_to_cart.is_enabled():
                pytest.fail(
                    "ADD TO CART UNAVAILABLE: The control is disabled."
                )

            print("PASS: Add to Cart control is available")

            # 6. Add product to cart
            await add_to_cart.click()

            # Amazon may show an add-to-cart confirmation or a side panel.
            # Continue to the cart directly to verify the actual contents.
            cart_link = page.locator("#nav-cart")

            await expect(cart_link).to_be_visible(timeout=20000)
            await cart_link.click()

            # 7. Validate cart contents
            cart_items = page.locator(
                "#sc-active-cart .sc-list-item"
            )

            await expect(cart_items.first).to_be_visible(timeout=30000)

            matching_cart_item = None

            for index in range(await cart_items.count()):
                item = cart_items.nth(index)

                item_text = (await item.inner_text()).strip()

                # Match a distinctive phrase from the selected product.
                if (
                    REQUIRED_PRODUCT_NAME.casefold()
                    in item_text.casefold()
                ):
                    matching_cart_item = item
                    break

            assert matching_cart_item is not None, (
                "CART VALIDATION FAILED: The expected product was not "
                "found in the active cart. It may not have been added, "
                "or Amazon may require sign-in."
            )

            print("PASS: Expected product found in cart")

            # Validate the cart item's visible title
            cart_title_locator = matching_cart_item.locator(
                ".sc-product-title"
            )

            if await cart_title_locator.count() == 0:
                cart_title_locator = matching_cart_item.locator(
                    "span.a-truncate-cut"
                )

            if await cart_title_locator.count() > 0:
                cart_title = (
                    await cart_title_locator.first.inner_text()
                ).strip()
                print(f"Cart product title: {cart_title}")

            # Validate quantity where the control is available
            quantity_control = matching_cart_item.locator(
                'select[name="quantity"]'
            )

            quantity = "Could not verify"

            if await quantity_control.count() > 0:
                quantity = await quantity_control.input_value()
                assert quantity == "1", (
                    f"EXPECTED QUANTITY 1, but cart quantity is "
                    f"{quantity}."
                )
            else:
                quantity_input = matching_cart_item.locator(
                    'input[name="quantity"]'
                )

                if await quantity_input.count() > 0:
                    quantity = await quantity_input.input_value()
                    assert quantity == "1", (
                        f"EXPECTED QUANTITY 1, but cart quantity is "
                        f"{quantity}."
                    )

            print(f"Cart quantity: {quantity}")

            # 8. Proceed to checkout entry point
            # This does not place an order or submit payment.
            checkout_button = page.locator(
                "#sc-buy-box-ptc-button"
            )

            if await checkout_button.count() == 0:
                print(
                    "CHECKOUT STOPPED: Proceed to checkout button "
                    "is unavailable. Check sign-in, cart state, or "
                    "Amazon's current page layout."
                )
                return

            await expect(checkout_button).to_be_visible(timeout=10000)
            await expect(checkout_button).to_be_enabled()
            await checkout_button.click()

            print(f"Checkout page opened: {page.url}")

            # 9. Safety boundary:
            # Do not automatically submit addresses, payment details,
            # or any final purchase action. If sign-in or other steps
            # are required, complete them manually in the opened browser.
            print(
                "\nSAFE CHECKOUT PAUSE:\n"
                "Complete any permitted checkout steps manually if "
                "Amazon requires them. Stop at the final order review "
                "page. Do NOT click Place your order / Buy now or "
                "submit payment."
            )

            input(
                "After reaching the final order review page "
                "(or if checkout is blocked), press Enter here..."
            )

            print(f"Current checkout URL: {page.url}")

            # Check for common final order controls without clicking them.
            final_order_control = page.get_by_role(
                "button",
                name=re.compile(
                    r"place your order|place order|buy now",
                    re.IGNORECASE
                )
            )

            if await final_order_control.count() > 0:
                print(
                    "FINAL REVIEW CHECK: A final purchase control "
                    "is present. It was NOT clicked."
                )
            else:
                print(
                    "FINAL REVIEW NOT CONFIRMED: The final purchase "
                    "control was not detected. Checkout may require "
                    "sign-in, address selection, payment setup, or "
                    "different selectors."
                )

            print("SAFE STOP: No order was placed by this test.")

        finally:
            await context.close()
            await browser.close()
