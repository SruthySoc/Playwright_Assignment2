
import pytest
from playwright.async_api import async_playwright, expect


# Replace these values with the trainer's requirements
SEARCH_KEYWORD = "wireless mouse"
REQUIRED_PRODUCT_NAME = "Logitech wireless mouse"


@pytest.mark.asyncio
async def test_find_and_validate_product_card():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # 1. Open Amazon India
            await page.goto(
                "https://www.amazon.in/",
                wait_until="domcontentloaded",
                timeout=60000
            )

            # 2. Search for the required keyword
            search_box = page.locator("#twotabsearchtextbox")
            await expect(search_box).to_be_visible(timeout=20000)

            await search_box.fill(SEARCH_KEYWORD)
            await search_box.press("Enter")

            # 3. Locate all product cards
            product_cards = page.locator(
                'div[data-component-type="s-search-result"]'
            )

            await expect(product_cards.first).to_be_visible(
                timeout=30000
            )

            card_count = await product_cards.count()
            print(f"Product cards found: {card_count}")

            # 4. Find a card by matching its visible product title
            matched_card = None
            matched_title = None

            for index in range(card_count):
                card = product_cards.nth(index)

                title_locator = card.locator("h2").first

                if await title_locator.count() == 0:
                    continue

                if not await title_locator.is_visible():
                    continue

                title = (await title_locator.inner_text()).strip()

                # Match by required product name/keyword
                if REQUIRED_PRODUCT_NAME.casefold() in title.casefold():
                    matched_card = card
                    matched_title = title
                    break

            # 5. Fail clearly if no matching card is found
            assert matched_card is not None, (
                f"PRODUCT NOT FOUND: No product card matched "
                f"'{REQUIRED_PRODUCT_NAME}' in Amazon search results "
                f"for '{SEARCH_KEYWORD}'. "
                f"Cards inspected: {card_count}"
            )

            print(f"Matched product title: {matched_title}")

            # 6. Validate the title inside the matched card
            matched_title_locator = matched_card.locator("h2").first
            await expect(matched_title_locator).to_contain_text(
                REQUIRED_PRODUCT_NAME,
                ignore_case=True
            )

            print("PASS: Product title validated in the matched card")

            # 7. Read price only from the matched card
            price_locator = matched_card.locator(
                ".a-price .a-offscreen"
            ).first

            if (
                await price_locator.count() > 0
                and await price_locator.is_visible()
            ):
                price = (await price_locator.inner_text()).strip()
            else:
                price = "Not visible"

            print(f"Product price: {price}")

            # 8. Interact only with a control inside the matched card
            # Open the matched product using its own title link
            product_link = matched_card.locator("h2 a").first

            await expect(product_link).to_be_visible()

            product_href = await product_link.get_attribute("href")
            assert product_href, (
                "MATCHED PRODUCT ERROR: Product link is missing "
                "inside the matched card."
            )

            # Click only the title link belonging to the matched card
            await product_link.click()

            # 9. Validate the product detail page
            await expect(page.locator("#productTitle")).to_be_visible(
                timeout=30000
            )

            detail_title = (
                await page.locator("#productTitle").inner_text()
            ).strip()

            print(f"Detail page title: {detail_title}")

            # Normalize whitespace and case before comparing titles
            normalize = lambda text: " ".join(text.split()).casefold()

            assert normalize(matched_title) == normalize(detail_title), (
                "TITLE MISMATCH: The search-result title does not match "
                "the product detail-page title.\n"
                f"Search result: {matched_title}\n"
                f"Detail page: {detail_title}"
            )

            print("PASS: Search result and detail-page titles match")
            print(f"Product URL: {page.url}")

        finally:
            await browser.close()
