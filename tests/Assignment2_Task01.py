
import asyncio
import csv
import os
from pathlib import Path

import pytest
from playwright.async_api import async_playwright, expect


# Keyword provided by the trainer
SEARCH_KEYWORD = "wireless mouse"

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / "test_data" / "selected_product.csv"


@pytest.mark.asyncio
async def test_amazon_product_search():

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

            await expect(
                page.locator("#twotabsearchtextbox")
            ).to_be_visible(timeout=20000)

            print("Amazon India opened successfully")

            # Step 2: Search for the trainer's keyword
            search_box = page.locator("#twotabsearchtextbox")
            await search_box.fill(SEARCH_KEYWORD)
            await search_box.press("Enter")

            await page.wait_for_load_state("domcontentloaded")

            results = page.locator(
                'div[data-component-type="s-search-result"]'
            )
            await expect(results.first).to_be_visible(timeout=30000)

            print(f"Search keyword: {SEARCH_KEYWORD}")

            # Step 3: Find a product by its visible title.
            # Do not select a product using a fixed result index.
            selected_title = None
            selected_url = None

            for i in range(await results.count()):
                product = results.nth(i)
                title_locator = product.locator("h2")

                if await title_locator.count() == 0:
                    continue

                title = (await title_locator.first.inner_text()).strip()

                if not title:
                    continue

                # Match all keyword words against the visible title.
                title_lower = title.casefold()
                keyword_words = SEARCH_KEYWORD.casefold().split()

                if not all(word in title_lower for word in keyword_words):
                    continue

                link = product.locator("h2 a").first
                href = await link.get_attribute("href")

                if href:
                    selected_title = title
                    selected_url = await page.evaluate(
                        "(href) => new URL(href, location.origin).href",
                        href
                    )
                    break

            assert selected_title, (
                f"No product title matched keyword: {SEARCH_KEYWORD}"
            )
            assert selected_url, "Product URL was not found"

            print(f"Selected product title: {selected_title}")
            print(f"Search result URL: {selected_url}")

            # Step 4: Open the selected product detail page
            await page.goto(
                selected_url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            detail_title_locator = page.locator("#productTitle")
            await expect(detail_title_locator).to_be_visible(
                timeout=30000
            )

            detail_title = (
                await detail_title_locator.inner_text()
            ).strip()

            print(f"Detail page title: {detail_title}")

            # Step 5: Validate title consistency
            normalize = lambda text: " ".join(text.split()).casefold()

            assert normalize(selected_title) == normalize(detail_title), (
                "Product title mismatch!\n"
                f"Search result: {selected_title}\n"
                f"Detail page: {detail_title}"
            )

            print("PASS: Search result and detail page titles match")

            # Step 6: Capture the product price when visible
            price = "Not visible"

            price_locator = page.locator(
                "#corePriceDisplay_desktop_feature_div "
                ".a-price .a-offscreen"
            ).first

            if await price_locator.count() > 0:
                if await price_locator.is_visible():
                    price_text = (await price_locator.inner_text()).strip()
                    if price_text:
                        price = price_text

            # Fallback for alternative Amazon price layouts
            if price == "Not visible":
                fallback_price = page.locator(
                    "#apex_desktop .a-price .a-offscreen"
                ).first

                if await fallback_price.count() > 0:
                    if await fallback_price.is_visible():
                        price_text = (
                            await fallback_price.inner_text()
                        ).strip()

                        if price_text:
                            price = price_text

            product_url = page.url

            # Step 7: Record product information in a CSV file
            OUTPUT_FILE.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            with open(
                OUTPUT_FILE,
                mode="w",
                newline="",
                encoding="utf-8-sig"
            ) as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=[
                        "search_keyword",
                        "product_title",
                        "price",
                        "product_url"
                    ]
                )

                writer.writeheader()
                writer.writerow({
                    "search_keyword": SEARCH_KEYWORD,
                    "product_title": detail_title,
                    "price": price,
                    "product_url": product_url
                })

            print("\n----- SELECTED PRODUCT DETAILS -----")
            print(f"Keyword     : {SEARCH_KEYWORD}")
            print(f"Title       : {detail_title}")
            print(f"Price       : {price}")
            print(f"Product URL : {product_url}")
            print(f"CSV file    : {OUTPUT_FILE}")
            print("------------------------------------")

        finally:
            await browser.close()
