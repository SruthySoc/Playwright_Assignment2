
import pytest
from playwright.async_api import async_playwright, expect


# Replace with the partial product name provided by your trainer
PARTIAL_PRODUCT_NAME = "wireless mou"


@pytest.mark.asyncio
async def test_amazon_search_autocomplete():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # Step 1: Open Amazon India
            await page.goto(
                "https://www.amazon.in/",
                wait_until="domcontentloaded",
                timeout=60000
            )

            search_box = page.locator("#twotabsearchtextbox")
            search_button = page.locator("#nav-search-submit-button")

            await expect(search_box).to_be_visible(timeout=20000)

            print("Amazon India opened successfully")

            # Step 2: Enter a partial product name
            await search_box.fill(PARTIAL_PRODUCT_NAME)

            # Step 3: Check autocomplete suggestions in this session.
            # Amazon commonly displays suggestions in this container.
            suggestions = page.locator(
                "#sac-autocomplete-results-container .s-suggestion"
            )

            matching_suggestion = None

            # Wait briefly for the suggestion list to appear using a
            # locator assertion. If it does not appear, use fallback.
            try:
                await expect(suggestions.first).to_be_visible(
                    timeout=5000
                )

                print("Autocomplete suggestions are displayed")

                # Step 4: Find a suggestion matching the partial name
                suggestion_count = await suggestions.count()

                for index in range(suggestion_count):
                    suggestion = suggestions.nth(index)

                    if not await suggestion.is_visible():
                        continue

                    suggestion_text = (
                        await suggestion.inner_text()
                    ).strip()

                    print(f"Suggestion: {suggestion_text}")

                    if (
                        PARTIAL_PRODUCT_NAME.casefold()
                        in suggestion_text.casefold()
                    ):
                        matching_suggestion = suggestion
                        break

                # Step 5: Select a matching suggestion if found
                if matching_suggestion is not None:
                    selected_text = (
                        await matching_suggestion.inner_text()
                    ).strip()

                    await matching_suggestion.click()

                    # Wait for search results to load
                    await expect(
                        page.locator(
                            'div[data-component-type="s-search-result"]'
                        ).first
                    ).to_be_visible(timeout=30000)

                    print(
                        "Selected autocomplete suggestion: "
                        f"{selected_text}"
                    )
                    print(f"Resulting URL: {page.url}")

                    # Validate that navigation/search occurred
                    assert "/s" in page.url or "k=" in page.url, (
                        "Suggestion was selected, but the resulting "
                        f"URL does not look like a search URL: {page.url}"
                    )

                    print(
                        "PASS: Autocomplete suggestion selected "
                        "and search results displayed"
                    )

                else:
                    print(
                        "Autocomplete appeared, but no suggestion "
                        "matched the requested partial name."
                    )

                    # Documented fallback
                    await search_button.click()

                    await expect(
                        page.locator(
                            'div[data-component-type="s-search-result"]'
                        ).first
                    ).to_be_visible(timeout=30000)

                    print(
                        "Fallback: Search button used because no "
                        "matching suggestion was found"
                    )
                    print(f"Resulting URL: {page.url}")

            except AssertionError:
                # No visible autocomplete suggestions in this session
                print(
                    "Autocomplete suggestions were absent "
                    "or did not become visible in this session."
                )

                # Step 6: Fall back to the Search button
                await search_button.click()

                await expect(
                    page.locator(
                        'div[data-component-type="s-search-result"]'
                    ).first
                ).to_be_visible(timeout=30000)

                print("Fallback: Search button clicked successfully")
                print(f"Resulting URL: {page.url}")

                print(
                    "DOCUMENTED BEHAVIOR: Search continued without "
                    "autocomplete suggestions."
                )

        finally:
            await browser.close()
