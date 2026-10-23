import asyncio
import re

from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeoutError,
)


AMAZON_URL = "https://www.amazon.in"
SEARCH_TERM = "wireless mouse"


async def test_product_state_retention():

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(15000)

        try:
            # STEP 1: Search for a product
            await page.goto(
                AMAZON_URL,
                wait_until="domcontentloaded"
            )

            search_box = page.locator("#twotabsearchtextbox")
            await search_box.wait_for(state="visible")
            await search_box.fill(SEARCH_TERM)
            await search_box.press("Enter")

            await page.locator(
                '[data-component-type="s-search-result"][data-asin]'
            ).first.wait_for(state="visible")

            # STEP 2: Capture the selected product BEFORE navigation
            results = page.locator(
                '[data-component-type="s-search-result"][data-asin]'
            )

            selected_product = results.first

            selected_asin = await selected_product.get_attribute(
                "data-asin"
            )

            selected_title = (
                await selected_product.locator("h2 a span")
                .first.inner_text()
            ).strip()

            search_url = page.url
            original_search_term = await search_box.input_value()

            assert selected_asin, "Selected product ASIN is empty."
            assert selected_title, "Selected product title is empty."

            print(f"Selected ASIN: {selected_asin}")
            print(f"Selected title: {selected_title}")

            # STEP 3: Open the product detail page
            await selected_product.locator("h2 a").first.click()

            await page.locator("#productTitle").wait_for(
                state="visible"
            )

            detail_title = (
                await page.locator("#productTitle").inner_text()
            ).strip()

            # Amazon product detail URLs usually contain /dp/ASIN
            detail_url = page.url
            match = re.search(
                r"/(?:dp|gp/product)/([A-Z0-9]{10})",
                detail_url
            )
            detail_asin = match.group(1) if match else None

            assert detail_title, "Product detail title is empty."

            assert (
                selected_title.casefold() in detail_title.casefold()
                or detail_title.casefold() in selected_title.casefold()
            ), (
                f"Product title mismatch: "
                f"{selected_title!r} != {detail_title!r}"
            )

            if detail_asin:
                assert detail_asin == selected_asin, (
                    f"ASIN mismatch: {selected_asin} != {detail_asin}"
                )

            # STEP 4: Add the product to the cart
            add_button = page.locator("#add-to-cart-button")
            await add_button.wait_for(state="visible")
            await add_button.click()

            # STEP 5: Navigate to the cart
            await page.goto(
                f"{AMAZON_URL}/gp/cart/view.html",
                wait_until="domcontentloaded"
            )

            # Wait for cart content; Amazon may use different markup
            await page.locator("body").wait_for(state="visible")

            cart_items = page.locator(
                '[data-asin], [data-itemid]'
            )

            # Check cart identifiers first
            cart_asins = await page.locator(
                '[data-asin]'
            ).evaluate_all(
                """elements => elements
                    .map(el => el.getAttribute('data-asin'))
                    .filter(Boolean)"""
            )

            cart_text = (
                await page.locator("body").inner_text()
            ).casefold()

            asin_in_cart = selected_asin in cart_asins
            title_in_cart = selected_title.casefold() in cart_text

            assert asin_in_cart or title_in_cart, (
                f"Selected product not found in cart. "
                f"ASIN={selected_asin}, title={selected_title}"
            )

            print("PASS: Selected product found in cart.")

            # STEP 6: Return to the original search results
            await page.goto(
                search_url,
                wait_until="domcontentloaded"
            )

            await page.locator(
                '[data-component-type="s-search-result"][data-asin]'
            ).first.wait_for(state="visible")

            # STEP 7: Verify the search context is retained
            restored_search = page.locator("#twotabsearchtextbox")

            restored_term = (
                await restored_search.input_value()
            ).strip()

            assert restored_term.casefold() == (
                original_search_term.strip().casefold()
            ), (
                f"Search term lost. Expected "
                f"{original_search_term!r}, got {restored_term!r}"
            )

            # Verify the originally selected product remains in results
            restored_product = page.locator(
                '[data-component-type="s-search-result"]'
                f'[data-asin="{selected_asin}"]'
            )

            assert await restored_product.count() > 0, (
                f"Selected product {selected_asin} is missing "
                "from the restored search results."
            )

            print("PASS: Search term retained.")
            print("PASS: Product retained in search results.")
            print("ALL ASSERTIONS PASSED.")

        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(test_product_state_retention())
