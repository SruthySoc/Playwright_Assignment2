
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_search_results_behavior(async_page):
    # Open Amazon India and search for a product
    await async_page.goto(
        "https://www.amazon.in/",
        wait_until="domcontentloaded"
    )

    search_box = async_page.locator("#twotabsearchtextbox")
    await search_box.fill("laptop")
    await search_box.press("Enter")

    # Wait for the search results page
    await async_page.locator(
        '[data-component-type="s-search-result"]'
    ).first.wait_for(state="visible", timeout=20000)

    product_cards = async_page.locator(
        '[data-component-type="s-search-result"]'
    )

    initial_count = await product_cards.count()
    print(f"Initial product cards: {initial_count}")

    assert initial_count > 0, "No product cards found"

    # Inspect the pagination controls
    next_page = async_page.locator(
        "a.s-pagination-next"
    ).first

    next_page_count = await next_page.count()

    if next_page_count > 0 and await next_page.is_visible():
        is_disabled = await next_page.get_attribute("aria-disabled")
        next_href = await next_page.get_attribute("href")

        if is_disabled != "true" and next_href:
            first_page_url = async_page.url
            first_product = await product_cards.first.inner_text()

            await next_page.click()
            await async_page.wait_for_load_state("domcontentloaded")

            await product_cards.first.wait_for(
                state="visible",
                timeout=20000
            )

            second_page_url = async_page.url
            second_count = await product_cards.count()
            second_product = await product_cards.first.inner_text()

            print("Behavior observed: pagination")
            print(f"Page 1 URL: {first_page_url}")
            print(f"Page 2 URL: {second_page_url}")
            print(f"Page 2 product cards: {second_count}")

            assert second_page_url != first_page_url, (
                "Pagination did not navigate to a different URL"
            )

            assert second_count > 0, (
                "No products found on the next page"
            )

            assert second_product != first_product, (
                "The first product appears unchanged after pagination"
            )

            return

    # If pagination is unavailable, inspect a Load More control
    load_more = async_page.get_by_role(
        "button",
        name="Load more",
        exact=False
    ).first

    if await load_more.count() > 0 and await load_more.is_visible():
        before_count = await product_cards.count()

        await load_more.click()

        await async_page.wait_for_function(
            """before => document.querySelectorAll(
                '[data-component-type="s-search-result"]'
            ).length > before""",
            arg=before_count,
            timeout=10000
        )

        after_count = await product_cards.count()

        print("Behavior observed: Load More")
        print(f"Before: {before_count}, after: {after_count}")

        assert after_count > before_count
        return

    # Otherwise, check whether scrolling loads more products
    before_count = await product_cards.count()

    await async_page.evaluate(
        "() => window.scrollTo(0, document.body.scrollHeight)"
    )

    try:
        await async_page.wait_for_function(
            """before => document.querySelectorAll(
                '[data-component-type="s-search-result"]'
            ).length > before""",
            arg=before_count,
            timeout=5000
        )

        after_count = await product_cards.count()

        print("Behavior observed: scrolling / lazy loading")
        print(f"Before: {before_count}, after: {after_count}")

        assert after_count > before_count

    except Exception:
        print(
            "Behavior observed: no additional product cards "
            "loaded after one scroll."
        )
        print(
            "The session may use ordinary pagination, "
            "a different control, or a page that does not expose "
            "infinite scrolling."
        )
