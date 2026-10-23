
import pytest
from playwright.async_api import async_playwright, expect


# Mock API source: this is NOT a real Amazon endpoint.
MOCK_API_ENDPOINT = "mock://trainer-product-api/products/123"


@pytest.fixture
def approved_product_api():
    """
    Mock response representing trainer-approved test API data.

    Replace these sample values with data supplied by your trainer
    or with the response from an approved public test API.
    """
    return {
        "source_endpoint": MOCK_API_ENDPOINT,
        "product": {
            "id": "123",
            "title": "Logitech Wireless Mouse",
        },
    }


def normalize_text(value):
    """Normalize whitespace and capitalization."""
    return " ".join(value.split()).casefold()


@pytest.mark.asyncio
async def test_amazon_product_title_matches_api(approved_product_api):

    api_response = approved_product_api

    # Read the API field being validated
    api_title = api_response["product"]["title"]
    product_id = api_response["product"]["id"]
    source_endpoint = api_response["source_endpoint"]
    api_field = "product.title"

    assert api_title, (
        f"API DATA ERROR: Field '{api_field}' is empty. "
        f"Source endpoint: {source_endpoint}"
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # Step 1: Open Amazon India
            await page.goto(
                "https://www.amazon.in/",
                wait_until="domcontentloaded",
                timeout=60000,
            )

            search_box = page.locator("#twotabsearchtextbox")
            await expect(search_box).to_be_visible(timeout=20000)

            # Step 2: Search using a keyword from the API title
            search_keyword = "Logitech Wireless Mouse"

            await search_box.fill(search_keyword)
            await search_box.press("Enter")

            product_cards = page.locator(
                'div[data-component-type="s-search-result"]'
            )

            await expect(product_cards.first).to_be_visible(
                timeout=30000
            )

            # Step 3: Find a product card matching the API title
            matched_card = None
            selected_ui_title = None

            for index in range(await product_cards.count()):
                card = product_cards.nth(index)
                title_locator = card.locator("h2").first

                if await title_locator.count() == 0:
                    continue

                if not await title_locator.is_visible():
                    continue

                visible_title = (
                    await title_locator.inner_text()
                ).strip()

                # Match by visible title, not by a fixed card index
                if (
                    normalize_text(api_title)
                    in normalize_text(visible_title)
                ):
                    link = card.locator("h2 a").first

                    if await link.get_attribute("href"):
                        matched_card = card
                        selected_ui_title = visible_title
                        break

            assert matched_card is not None, (
                "PRODUCT NOT FOUND\n"
                f"API endpoint: {source_endpoint}\n"
                f"API field: {api_field}\n"
                f"API product ID: {product_id}\n"
                f"Expected API title: '{api_title}'\n"
                f"Search keyword: '{search_keyword}'\n"
                "No visible Amazon result title contained the API title."
            )

            # Step 4: Open the matching product detail page
            await matched_card.locator("h2 a").first.click()

            detail_title_locator = page.locator("#productTitle")

            await expect(
                detail_title_locator
            ).to_be_visible(timeout=30000)

            ui_title = (
                await detail_title_locator.inner_text()
            ).strip()

            # Step 5: Compare API and UI values
            normalized_api_title = normalize_text(api_title)
            normalized_ui_title = normalize_text(ui_title)

            # Step 6: Report comparison details
            print("\n========== API vs UI VALIDATION ==========")
            print(f"API endpoint : {source_endpoint}")
            print(f"API field    : {api_field}")
            print(f"API product ID: {product_id}")
            print(f"UI field     : #productTitle")
            print(f"API title    : {api_title}")
            print(f"UI title     : {ui_title}")
            print(f"Product URL  : {page.url}")

            assert normalized_api_title == normalized_ui_title, (
                "\nPRODUCT TITLE MISMATCH\n"
                f"API endpoint: {source_endpoint}\n"
                f"API field: {api_field}\n"
                f"UI field: #productTitle\n"
                f"Expected (API): '{api_title}'\n"
                f"Actual (UI): '{ui_title}'\n"
                f"Normalized API value: '{normalized_api_title}'\n"
                f"Normalized UI value: '{normalized_ui_title}'"
            )

            print("RESULT: PASS - API title matches UI title")
            print("=========================================\n")

        finally:
            await browser.close()
