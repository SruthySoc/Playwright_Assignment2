# Playwright_Assignment2

Using an authorized test account, sign in only if permitted by the trainer and the site terms.
Save the authenticated browser context state to a local file using Playwright storage_state.
Create a new browser context using the saved state and verify the expected authenticated state without repeating the sign-in flow.
Handle expired sessions gracefully by detecting the sign-in page and reporting that re-authentication is needed.
Never include the storage-state file in Git, email, or the student submission; treat it as a credential secret.
For your Playwright Python assignment, you can use storage_state() to save an authorized test session and reuse it in a new browser context without repeating the sign-in process.

Security rule: use only a trainer-approved test account and permitted test website. The storage-state file may contain cookies and tokens that grant account access, so keep it local and never commit or share it.

1. Project structure
Playwright_Python_Folder/
├── tests/
│   └── test_auth_state.py
├── .auth/
│   └── storage_state.json
├── .gitignore
└── requirements.txt
The .auth/storage_state.json file is generated locally and must not be included in your submission.

2. Create the async pytest test
Create tests/test_auth_state.py. Replace the example URL and selectors with those from your trainer-approved test application. This example does not automate Amazon sign-in or store credentials in code.


import json
from pathlib import Path

import pytest
from playwright.async_api import async_playwright


APP_URL = "https://your-authorized-test-app.example/"
STATE_FILE = Path(".auth/storage_state.json")

# Replace these with selectors from your approved test app.
SIGN_IN_SELECTOR = 'input[name="username"]'
AUTHENTICATED_SELECTOR = '[data-testid="account-menu"]'


def is_sign_in_url(url):
    return "/login" in url.lower() or "/signin" in url.lower()


@pytest.mark.asyncio
async def test_reuse_authenticated_state():
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        # 1. Open the authorized application.
        original_context = await browser.new_context()
        page = await original_context.new_page()
        await page.goto(APP_URL)

        # 2. Sign in only when explicitly permitted.
        # Complete the approved sign-in manually if required.
        if is_sign_in_url(page.url):
            print("Sign-in required. Complete approved login.")

What to customize
APP_URL: the home or dashboard URL of your authorized test application.

SIGN_IN_SELECTOR: the example username-field selector; adjust it for your application. The sample declares it for reference, but does not use it to automate login.

AUTHENTICATED_SELECTOR: an element visible only when the user is signed in, such as an account menu or dashboard element.

is_sign_in_url(): adapt the URL checks to the application's actual sign-in routes.

The code uses a manual pause when the app redirects to sign-in. Complete authentication only if your trainer authorizes it. If your trainer provides a pre-authenticated test context, use that instead.

3. Protect the state file with .gitignore
Add these lines to the .gitignore file at your project root:


# Playwright authentication secrets
.auth/
storage_state.json
Check whether the file is already tracked:

git status --short
git check-ignore -v .auth/storage_state.json

If it was previously committed, adding it to .gitignore alone does not remove it from Git tracking. Remove it from the index with:

git rm --cached .auth/storage_state.json

Then commit the .gitignore change. If the state file was pushed previously, revoke or invalidate the associated session as appropriate; deleting the file from a later commit does not remove it from Git history.

4. Run the test
python -m pytest -s -v tests/test_auth_state.py

Expected output when successful:

Authenticated state saved locally.
PASS: New context reused the authenticated state without repeating the sign-in flow.
A restored session can still fail if authentication has expired, the server requires additional checks, or the application stores session data outside browser storage. storage_state() saves supported cookies and local storage, and optionally IndexedDB in supported Playwright versions; it does not save every possible browser-session mechanism.

Assignment outcome: the test saves the authorized session, opens a new context from the saved state, verifies authentication, and reports when re-authentication is needed—without placing the secret state file in your GitHub repository.

Create a setup script or fixture that saves browser state after an authorized sign-in.
Create a separate test that loads the saved state in a new browser context.
Validate a harmless authenticated page or account indicator.
Run the test again to confirm session reuse, then test the expired/missing state-file scenario.
Keep state files local and add them to .gitignore.
You can organize this assignment into two separate async Playwright tests: one saves browser state after an authorized sign-in, and the other loads that state in a new browser context and verifies that the session is still authenticated.

We'll also test what happens when the state file is missing or the saved session has expired. Use your trainer-approved test application and account; don't use real account credentials or submit any orders.

1. Project structure
Playwright_Python_Folder/
├── tests/
│   ├── test_save_state.py
│   └── test_reuse_state.py
├── .auth/
│   └── storage_state.json
├── .gitignore
└── requirements.txt
Install the required packages if needed:

pip install pytest pytest-asyncio playwright
playwright install chromium

2. Create the setup script
Create setup_auth_state.py in your project root. It opens the authorized application, lets you complete sign-in manually if permitted, verifies an authenticated account indicator, and saves the state locally.


import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

APP_URL = "https://your-authorized-test-app.example/"
AUTH_INDICATOR = '[data-testid="account-menu"]'
STATE_FILE = Path(__file__).parent / ".auth" / "storage_state.json"


async def main():
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(APP_URL)

            print("Complete authorized sign-in if required.")
            print("Do not enter real personal or payment data.")

            # Complete the approved sign-in manually.
            # Resume the script after sign-in.
            await page.pause()

            # Save state only after authentication is verified.
            await page.locator(AUTH_INDICATOR).wait_for(
                state="visible",
                timeout=10000
            )

            await context.storage_state(path=str(STATE_FILE))
            print(f"Browser state saved to: {STATE_FILE}")

        finally:
            await context.close()
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())


Replace APP_URL and AUTH_INDICATOR with the values from your approved test application. If the application is already authenticated, you can remove the manual pause.

Run the setup script:

python setup_auth_state.py

Complete the permitted sign-in, then resume execution in the Playwright Inspector. The script should create .auth/storage_state.json.

3. Create a separate state-reuse test
Create tests/test_reuse_state.py. This test loads the saved state into a new browser context and checks a harmless authenticated account indicator without repeating sign-in.




@pytest.mark.asyncio
async def test_reuse_saved_authentication():
    if not STATE_FILE.is_file():
        pytest.fail(
            f"Missing state file: {STATE_FILE}. "
            "Run setup_auth_state.py first."
        )

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        try:
            context = await browser.new_context(
                storage_state=str(STATE_FILE)
            )
            page = await context.new_page()

            try:
                await page.goto(
                    APP_URL,
                    wait_until="domcontentloaded"
                )

                # Detect a redirect to sign-in.
                if any(path in page.url.lower()
                       for path in LOGIN_PATHS):
                    pytest.fail(
                        "Saved session expired. "
                        "Authorized re-authentication is needed."
                    )

                # Verify that the authenticated indicator appears.
                try:
                    await page.locator(
                        AUTH_INDICATOR
                    ).wait_for(
                        state="visible",
                        timeout=10000
                    )
                except Exception:
                    pytest.fail(
                        "Authenticated state not confirmed. "
                        "The session may have expired, or the "
                        "account indicator selector may be incorrect."
                    )

                print(
                    "PASS: Authenticated state reused in "
                    "a new browser context."
                )

            finally:
                await context.close()

        finally:
            await browser.close()


def require_state_file(path):
    if not path.is_file():
        raise FileNotFoundError(
            f"Authentication state missing: {path}. "
            "Run setup_auth_state.py first."
        )


def test_missing_state_file_handled():
    missing_file = STATE_FILE.parent / "missing_state.json"

    with pytest.raises(
        FileNotFoundError,


The missing-file test deliberately checks a separate, nonexistent filename. It doesn't delete your real state file.

4. Keep authentication state out of Git
Add this to your project-root .gitignore:


# Playwright authentication state: secret credentials
.auth/
storage_state.json
Verify that Git ignores the state file:

git check-ignore -v .auth/storage_state.json
git status --short

If the state file was previously tracked, remove it from the Git index:

git rm --cached .auth/storage_state.json

This leaves the local file in place. If the file was already pushed to GitHub, invalidate the associated session and treat the credential as exposed.

5. Run the tests in order
First — save state

python setup_auth_state.py

Expected: .auth/storage_state.json is created after authentication is verified.

Second — reuse state

python -m pytest -s -v tests/test_reuse_state.py

Expected: the account indicator is visible in the new context, and the missing-file test passes.

Third — test missing state

Rename .auth/storage_state.json temporarily, run the reuse test, and verify that it reports the missing file clearly. Restore the file afterward. The missing-file test itself uses a separate filename and should pass independently.

Expected behavior: a valid saved session opens the authenticated page without another sign-in. A missing state file produces a clear setup error, while an expired session reports that authorized re-authentication is needed. A timeout on the account indicator alone cannot prove the session expired; verify the selector and actual page state before concluding.

please create README file for the below


Task 1 – End-to-End Product Discovery

Open Amazon India and search for a product using a keyword provided by the trainer.
Select a product by matching its visible title, not by using a hard-coded product position.
Open the product detail page and validate that the product title is consistent with the selected search result.
Record the selected product title, price when visible, and product URL.
Task 2 – Dynamic Product Selection with Robust Locators

Find all product cards displayed in search results.
Identify a card by matching a required product name or keyword.
Within that card, validate the title and interact with an available control only inside the matched card.
Avoid fragile absolute XPath and selectors based only on changing item indexes.
Handle the case where no matching product is found with a clear test failure message.
Task 3 – Auto-Suggest Dropdowns with Dynamic Waiting

Enter a partial product name into Amazon's search box.
Check whether autocomplete suggestions are shown in the current session.
If suggestions appear, wait for the suggestion list, select the matching suggestion, and validate the resulting search term or navigation.
If suggestions are absent, continue using the Search button and document the behavior.
Do not use fixed sleeps as the main synchronization method; use locator waits or expect assertions.
Task 4 – Checkout Journey (Stop Before Purchase)

Search for a product and open its detail page.
Validate product title and availability of the Add to Cart control.
Add the product to the cart if the session allows it.
Open the cart and validate the item name and quantity.
Proceed through any permitted checkout screens only as far as the final review stage. Do not click the final place-order/purchase button or submit payment.
Task 5 – UI and API Data Validation

Choose a product field that can be verified from an approved public or trainer-provided test API, such as product title, identifier, or price.
Retrieve the API data using an approved endpoint or mock service.
Compare the API value with the corresponding UI value after normalizing whitespace and currency formatting where appropriate.
Report mismatches clearly and include the source endpoint and field names in the test report.
If no approved API exists for the chosen Amazon page, create a mock API fixture or use a trainer-approved API; do not reverse-engineer or depend on private endpoints.
Task 6 – Managing State Across Multiple Pages

Search for a product and open its detail page.
Capture the selected product identifier or title before navigation.
Navigate to the cart and validate that the same product is present.
Navigate back to search results or another permitted page and verify that the chosen search context or product information is retained where expected.
Use explicit assertions to detect unexpected state loss.
Task 7 – Pagination and Infinite Scroll

Inspect search results to determine whether the current page uses pagination, a Load More control, or scrolling.
For pagination, navigate to the next available results page and validate that the result set changes.
For infinite scroll or lazy-loaded results, scroll and wait until new product cards appear.
Avoid assuming Amazon always uses one pagination pattern; record the behavior seen in your session.
If the live page does not expose the needed pattern, demonstrate the missing behavior on a trainer-approved test page.
Task 8 – Multi-Step Forms and Data Persistence

Use a permitted Amazon form flow, such as a non-sensitive address-form demonstration, only if the trainer has provided an authorized test account and safe test data.
Enter test data into the available steps and move forward/backward where possible.
Validate which fields remain populated after navigation between steps.
Do not save real personal information or submit an actual order.
If no safe form flow is available, demonstrate persistence on a trainer-provided mock checkout form and explain the expected behavior.
Task 9 – Conditional Execution Based on UI State

Check whether the product is in stock and whether Add to Cart is enabled.
If the control is visible and enabled, continue to the cart validation step.
If it is missing or disabled, record the product as unavailable and skip cart-dependent steps with a clear reason.
Use conditional checks based on current UI state rather than suppressing failures.
Task 10 – Global Authentication Using Storage State

Using an authorized test account, sign in only if permitted by the trainer and the site terms.
Save the authenticated browser context state to a local file using Playwright storage_state.
Create a new browser context using the saved state and verify the expected authenticated state without repeating the sign-in flow.
Handle expired sessions gracefully by detecting the sign-in page and reporting that re-authentication is needed.
Never include the storage-state file in Git, email, or the student submission; treat it as a credential secret.
Task 11 – Reuse Browser Session Across Test Runs

Create a setup script or fixture that saves browser state after an authorized sign-in.
Create a separate test that loads the saved state in a new browser context.
Validate a harmless authenticated page or account indicator.
Run the test again to confirm session reuse, then test the expired/missing state-file scenario.
Keep state files local and add them to .gitignore.
Task 12 – Mini Project and Execution Report

Combine product search, robust selection, cart validation, conditional execution, and session reuse into a small Pytest suite.
Use reusable fixtures and helper functions where appropriate.
Produce a summary of passed, failed, and skipped tests.
Attach screenshots for failures and explain the root cause and proposed correction.
…
Here is a complete README.md for your Amazon India Playwright Automation Project, covering all 12 tasks, installation, project structure, execution instructions, reporting, and security practices.

Create a file named README.md in your Playwright_Python_Folder project root and paste the following content.


















































































































































Before you push to GitHub
Check that your README.md accurately describes the files you have implemented and that the authentication state is not staged.

git status

Your README.md is ready to save as the project documentation.

please make it in comprehensive manner
Here is a more comprehensive, professional README.md for your Amazon India – Playwright Python Automation Project. It includes all 12 tasks, detailed objectives, project architecture, installation, execution commands, testing strategy, reporting, troubleshooting, GitHub setup, and security guidelines.

Save this as README.md in the root of your Playwright_Python_Folder project.

Amazon India – End-to-End Web Automation Framework
1. Project Overview
This project is designed to demonstrate practical web automation using Python, Playwright, and Pytest. It covers end-to-end product discovery, dynamic web elements, search suggestions, cart validation, API and UI data verification, state management, pagination, form persistence, conditional execution, authentication reuse, and test reporting.

The project is organized around 12 automation tasks that reflect common challenges encountered in modern web applications.

Amazon India is used as the primary learning website where permitted. Trainer-approved mock applications and test APIs are used whenever a live website does not expose the required behavior or when a controlled test environment is necessary.

The automation framework emphasizes:

Reliable and maintainable locator strategies.

Asynchronous browser interactions.

Explicit assertions and meaningful failure messages.

Dynamic waiting instead of arbitrary fixed delays.

Reusable fixtures and helper functions.

Conditional execution based on actual application state.

Secure browser-session management.

Clear test execution reports and failure evidence.

Important: All testing must comply with the trainer's authorization, the website's terms, and applicable access restrictions. The framework must not place real orders, submit payments, bypass security controls, or expose credentials.

2. Project Objectives
The primary objectives of this project are to:

Automate product search and validate product details.

Identify products dynamically by visible title or keyword.

Implement robust locators scoped to individual product cards.

Handle autocomplete suggestions using dynamic waits.

Validate the shopping cart without completing a purchase.

Compare UI values with approved API or mock-service data.

Verify product identity and context across page navigation.

Detect pagination, Load More controls, and lazy-loaded results.

Verify form data persistence across multi-step navigation.

Execute cart-dependent steps conditionally based on product availability.

Save and reuse authenticated browser state securely.

Produce execution summaries, screenshots, and actionable failure reports.

3. Technology Stack
Technology	Purpose
Python	Programming language for the automation framework
Playwright	Browser automation and web interaction
Pytest	Test discovery, execution, fixtures, assertions, and reporting
pytest-asyncio	Support for asynchronous test functions
Chromium	Browser used for automated execution
HTTP/API client	Access to approved API or mock-service data
pytest-html	Optional HTML test reports
Git	Source-code version control
GitHub	Remote repository and project collaboration
PyCharm	Development environment
Key automation concepts
Async automation: Uses async and await to coordinate browser operations.

Fixtures: Provide reusable browser pages, contexts, and test setup.

Locators: Identify elements using accessible roles, labels, text, and stable attributes.

Assertions: Validate expected application behavior.

Browser context: Isolates cookies, storage, and session data between tests.

Storage state: Saves supported browser authentication data for reuse.

Conditional execution: Runs dependent steps only when their prerequisites are satisfied.

4. Project Architecture
Recommended directory structure
Playwright_Python_Folder/
│
├── tests/
│   ├── test_task01_product_discovery.py
│   ├── test_task02_dynamic_locators.py
│   ├── test_task03_autosuggest.py
│   ├── test_task04_checkout_journey.py
│   ├── test_task05_api_ui_validation.py
│   ├── test_task06_state_management.py
│   ├── test_task07_pagination.py
│   ├── test_task08_form_persistence.py
│   ├── test_task09_conditional_execution.py
│   ├── test_task10_global_authentication.py
│   ├── test_task11_session_reuse.py
│   └── test_task12_mini_project.py
│
├── configuration/
│   └── config.py
│
├── test_data/
│   └── test_data.json
│
├── utilities/
│   └── helpers.py
│
├── .auth/
│   └── storage_state.json
│
├── reports/
│
├── screenshots/
│
├── conftest.py
├── pytest.ini
├── requirements.txt
├── .gitignore
└── README.md
This structure is a recommended layout, not a claim that every file already exists. Create the files as the corresponding tasks are implemented.

Directory responsibilities
tests/

Contains the individual task tests and the integrated mini-project test.

configuration/

Stores non-sensitive configuration such as application URLs, timeouts, browser settings, and approved environment options.

test_data/

Stores reusable synthetic product keywords and other non-sensitive test data.

utilities/

Contains reusable helper functions for locating products, normalizing values, capturing screenshots, and validating results.

conftest.py

Defines shared Pytest fixtures for browser setup, pages, contexts, and common test configuration.

.auth/

Contains local authentication state files. These files are sensitive and must never be committed or submitted.

reports/

Stores generated execution reports.

screenshots/

Stores screenshots captured for test failures.

requirements.txt

Lists the Python packages required by the project.

.gitignore

Excludes virtual environments, caches, authentication secrets, and generated artifacts from Git.

5. Installation and Environment Setup
5.1 Prerequisites
Install the following tools before running the project:

Python 3.10 or another version supported by the selected dependencies.

PyCharm or a compatible Python IDE.

Git.

An operating-system-compatible browser installation managed by Playwright.

Access to any trainer-approved test application or API required by the tasks.

Use a Python version supported by all installed packages, including Playwright and pytest-asyncio.

5.2 Create a virtual environment
On Linux:

python3 -m venv .venv
source .venv/bin/activate
On Windows PowerShell:

python -m venv .venv
.venv\Scripts\Activate.ps1
A virtual environment keeps project dependencies separate from system-wide Python packages.

5.3 Create requirements.txt
pytest
pytest-asyncio
playwright
pytest-html
If API tests use an additional HTTP client, include its package only when needed.

Install the dependencies:

python -m pip install -r requirements.txt
Install the Chromium browser:

python -m playwright install chromium
Verify the installation:

python --version
python -m pytest --version
python -m playwright --version
5.4 Configure asynchronous Pytest execution
Create pytest.ini in the project root:

[pytest]
asyncio_mode = auto
testpaths = tests
addopts = -v
This configuration enables automatic handling of supported asyncio tests. If the project uses a different asyncio mode or shared event-loop fixture strategy, configure it consistently with the installed pytest-asyncio version.

6. Task-by-Task Implementation Details
Task 1 – End-to-End Product Discovery
Objective: Search for a product, identify it by its visible title, open its details page, and capture its information.

Implementation steps:

Open Amazon India or the authorized test application.

Enter a keyword provided by the trainer.

Submit the search.

Wait for the product cards to appear.

Inspect the visible titles and identify the required product.

Click the matching product title or product link.

Wait for the detail page to load.

Verify that the detail-page title corresponds to the selected search-result title.

Capture the product title, displayed price if available, and current URL.

Validation criteria:

Search results are displayed.

A matching product is found.

The product detail page is opened.

The selected product's identity remains consistent.

The title, price, and URL are recorded where available.

Expected outcome: The test discovers a product dynamically and records its details without depending on a fixed result position.

Task 2 – Dynamic Product Selection with Robust Locators
Objective: Select the correct product using stable locators and card-level scoping.

Implementation steps:

Locate the product cards displayed in the results.

Iterate through the cards or filter them using a matching title locator.

Identify the card containing the required product name or keyword.

Validate the title within that card.

Interact with the relevant link or control inside the matched card.

Fail clearly if no matching card exists.

Locator guidelines:

Prefer:

get_by_role()

get_by_label()

get_by_text()

locator() with stable attributes

Locators scoped to the matched product card

Avoid:

Long absolute XPath expressions.

Fragile selectors that depend entirely on changing indexes.

Global buttons when the intended button belongs to a specific card.

Expected outcome: The intended product is selected reliably, and missing products produce a meaningful test failure.

Task 3 – Auto-Suggest Dropdowns with Dynamic Waiting
Objective: Handle search autocomplete based on the behavior observed in the current session.

Implementation steps:

Locate the search box.

Enter a partial product name.

Inspect whether suggestions appear.

If suggestions are available, wait for the suggestion list.

Select the suggestion matching the requested keyword.

Verify the resulting search term or navigation.

If suggestions are absent, submit the search through the available Search button or keyboard action.

Record whether autocomplete appeared.

Synchronization strategy:

Use Playwright locator waits, visibility checks, and expect() assertions.

Avoid using fixed delays as the main synchronization mechanism.

Expected outcome: The test supports both autocomplete-enabled and autocomplete-unavailable sessions.

Task 4 – Checkout Journey (Stop Before Purchase)
Objective: Validate the permitted product-to-cart journey without placing an order.

Implementation steps:

Search for a product and open its detail page.

Validate the product title.

Inspect the availability information.

Verify that Add to Cart is present, visible, and enabled.

Add the product only when the application and test conditions permit it.

Navigate to the cart.

Validate the product name and quantity.

Continue through permitted checkout screens only as far as the final review stage.

Stop before the final Place Order or purchase action.

Validation criteria:

The selected product is available for the permitted test.

The cart contains the expected item.

The quantity matches the expected value.

The correct product remains selected throughout the journey.

Expected outcome: Cart and permitted checkout behavior are validated without completing a transaction.

Task 5 – UI and API Data Validation
Objective: Compare a product field displayed in the UI against a value from an approved API or mock service.

Possible fields:

Product title.

Product identifier.

Price, when both sources represent the same price and currency.

Implementation steps:

Select a field that has a trusted reference value.

Request the value from an approved public or trainer-provided API.

Capture the corresponding UI value.

Normalize whitespace and other permitted formatting differences.

Compare the normalized values.

Report mismatches with the endpoint, field names, expected value, and actual value.

Example normalization:

def normalize_text(value):
    return " ".join(value.split())
Price normalization should account for currency symbols, separators, and numeric precision only when those transformations preserve the meaning of the values being compared.

Expected outcome: Differences between the UI and the approved reference data are reported clearly.

Important: Do not reverse-engineer private endpoints or assume that a live retail price is guaranteed to match a mock or public API. If no approved reference exists, use a trainer-provided API or controlled mock service.

Task 6 – Managing State Across Multiple Pages
Objective: Verify that product identity and relevant search context are retained during navigation.

Implementation steps:

Search for a product.

Select a product and capture its title or identifier.

Open the detail page.

Navigate to the cart when permitted.

Verify that the same product appears in the cart.

Return to search results or another permitted page.

Validate the expected search context or product information.

Use explicit assertions to detect unexpected state loss.

Expected outcome: Product identity is tracked across navigation, and unexpected state changes are detected.

Task 7 – Pagination and Infinite Scroll
Objective: Identify and test the result-loading behavior exposed in the current session.

Implementation steps:

Inspect the result page for pagination controls.

Check whether a Load More control is available.

Observe whether scrolling loads additional product cards.

If pagination is present, navigate to the next page and compare the result sets.

If lazy loading is present, scroll and wait for new cards to appear.

Record the observed behavior.

If the required behavior is absent on the live page, demonstrate it using an approved test page.

Validation criteria:

The observed loading pattern is recorded.

The next page contains a changed result set when pagination is tested.

Additional cards appear when lazy loading is successfully triggered.

The test does not claim that infinite scrolling is absent solely because one scroll produced no new cards.

Expected outcome: The test adapts to the current result-loading pattern instead of assuming one fixed implementation.

Task 8 – Multi-Step Forms and Data Persistence
Objective: Validate whether form values remain populated when moving between steps.

Implementation steps:

Use an authorized form flow or trainer-provided mock checkout page.

Enter synthetic test data.

Move forward to the next step.

Populate the available fields.

Navigate backward.

Validate whether earlier fields retain their values.

Navigate forward again.

Verify the expected values in the later step.

Validation criteria:

Fields are populated with the intended test values.

Values are checked after each navigation step.

Unexpected resets are detected through assertions.

No real personal information is saved.

No actual order is submitted.

Expected outcome: Form persistence is demonstrated safely in a controlled test environment.

Task 9 – Conditional Execution Based on UI State
Objective: Run cart-dependent actions only when product availability and control state allow them.

Implementation steps:

Inspect the product's availability message.

Check whether Add to Cart exists.

Check whether the control is visible.

Check whether it is enabled.

Continue to the cart only when the prerequisites are satisfied.

If the product is explicitly unavailable or the required control cannot be used, record the observed state and skip dependent steps with a clear reason.

Investigate unexpected application states rather than suppressing errors.

Important distinction:

A missing or disabled button does not always prove that a product is out of stock. The page may still be loading, a product variation may be required, or another interaction may be necessary.

Expected outcome: The test handles known unavailable conditions explicitly while preserving genuine failures.

Task 10 – Global Authentication Using Storage State
Objective: Save authorized authentication state and verify that a new browser context can reuse it.

Implementation steps:

Use a trainer-authorized test account.

Complete the permitted authentication flow.

Verify that the authenticated page or account indicator is visible.

Save supported browser state using Playwright's storage_state() method.

Create a new browser context using the saved state.

Open a harmless authenticated page.

Verify that the expected authenticated indicator appears.

Detect redirects to sign-in and report when re-authentication is required.

Expected outcome: The test demonstrates session reuse without repeating sign-in when the saved session is still valid.

Security requirement: Authentication state may contain cookies and tokens that grant access to an account. Never commit, email, upload, or submit the state file.

Task 11 – Reuse Browser Session Across Test Runs
Objective: Separate session setup from session reuse and validate both normal and exceptional cases.

Implementation steps:

Create a setup script or fixture that saves state after authorized authentication.

Create a separate test that loads the saved state.

Open a new browser context.

Validate a harmless authenticated page or account indicator.

Run the test again to confirm that the saved state is reused.

Test a missing state-file scenario.

Test an expired-session scenario where supported by the approved application.

Verify that re-authentication is reported clearly.

Expected outcome: Session persistence and recovery behavior are tested independently.

Note: Reusing a storage-state file does not guarantee that a session will remain valid indefinitely. The server may expire or revoke it.

Task 12 – Mini Project and Execution Report
Objective: Combine the reusable automation components into a maintainable test suite.

Recommended components:

Product search and selection.

Robust product-card locators.

Product detail validation.

Conditional Add to Cart behavior.

Cart content verification.

Navigation and state validation.

Authorized authentication-state reuse.

Failure screenshots.

Test execution reporting.

Implementation steps:

Refactor repeated interactions into helper functions.

Define shared fixtures for browser and page setup.

Use configuration files for non-sensitive settings.

Store synthetic test data separately.

Add explicit assertions for expected behavior.

Execute the suite using Pytest.

Generate a summary of passed, failed, skipped, and errored tests.

Capture screenshots for relevant failures.

Document root causes and proposed corrections.

Expected outcome: A small but maintainable automation framework with reproducible tests and useful execution evidence.

7. Configuration and Reusable Components
7.1 Configuration
Store non-sensitive settings in configuration/config.py.

Example:

BASE_URL = "https://www.amazon.in/"
DEFAULT_TIMEOUT = 10000
BROWSER_NAME = "chromium"
HEADLESS = True
These values are examples. Adapt them to the approved test environment.

Do not store passwords, access tokens, or authentication-state contents in configuration files.

7.2 Test data
Store reusable, non-sensitive test values in test_data/test_data.json.

Example:

{
  "search_keyword": "laptop",
  "required_product_keyword": "laptop",
  "expected_quantity": 1
}
Use keywords and values approved for the assignment. Do not assume that a particular product is always available or has a fixed price.

7.3 Fixtures
Use conftest.py for shared Pytest fixtures.

Possible fixtures include:

Browser or browser context.

Page instance.

Test data.

Approved application configuration.

Screenshot-on-failure support.

Authentication-state loading.

Choose fixture scopes deliberately. Function-scoped contexts are useful when tests require isolation, while shared session state should be reused only where appropriate and authorized.

7.4 Helper functions
Place reusable functions in utilities/helpers.py.

Possible helpers include:

Product-card selection by title.

Product-title normalization.

Price normalization.

Product URL and title capture.

Availability detection.

Screenshot capture.

Authentication-state validation.

Keep helpers focused and ensure that failures remain visible to the calling test.

8. Test Execution Guide
Activate the virtual environment before executing tests.

Run the entire suite
python -m pytest -v
Display print() output in the terminal
python -m pytest -s -v
Run a specific task
python -m pytest -s -v tests/test_task01_product_discovery.py
Run tests matching a keyword
python -m pytest -v -k "pagination"
Generate an HTML report
First, ensure the reports/ directory exists. Then run:

python -m pytest -v \
  --html=reports/report.html \
  --self-contained-html
On Windows PowerShell, the same command can be entered on one line:

python -m pytest -v --html=reports/report.html --self-contained-html
The report provides a convenient summary of test execution. Review it before sharing, and remove sensitive values or screenshots if any were captured.

9. Execution Results and Reporting
The framework should distinguish the following outcomes:

Status	Description
Passed	The expected behavior was verified.
Failed	An assertion or test condition did not meet expectations.
Skipped	A documented prerequisite was unavailable or the test was intentionally not applicable.
Error	Test setup, fixture initialization, or another execution-stage problem prevented normal completion.
Recommended failure evidence
For each failed test, record:

Task number and test name.

Expected behavior.

Actual behavior.

Assertion message or exception.

Relevant screenshot path.

Root cause, if known.

Proposed correction.

Whether the failure is reproducible.

Capture screenshots only when they are useful and permitted. Avoid including credentials, personal addresses, payment details, authentication tokens, or other sensitive information.

Do not classify an unexpected error as a skip simply to obtain a passing report.

10. Authentication and Session Security
Browser storage state is sensitive because it may contain cookies, tokens, and other session information.

Follow these practices:

Use only trainer-authorized test accounts.

Save state files only in the local project environment.

Add authentication-state paths to .gitignore.

Never include storage-state files in the student submission.

Never send state files through email or messaging applications.

Avoid printing cookies, tokens, passwords, or storage contents in logs.

Verify that the state file is ignored by Git.

Invalidate the associated session if the file is exposed.

Use a new browser context for isolated tests where appropriate.

Detect expired sessions and report when authorized re-authentication is required.

Example .gitignore
# Python
__pycache__/
*.py[cod]
.venv/
venv/

# Pytest
.pytest_cache/

# IDE
.idea/

# Authentication secrets
.auth/
storage_state.json

# Generated test artifacts
reports/
screenshots/
Adding a file to .gitignore does not remove it from Git tracking if it was already committed. Previously exposed state files should be treated as compromised even if they are deleted from a later commit.

11. Troubleshooting
Product not found
Possible causes:

Search results differ by session.

The requested product is unavailable.

The title-matching rule is too restrictive.

The page has not finished loading.

Recommended action: Inspect the visible product titles, confirm the locator, and report a clear failure when no matching product exists.

Locator timeout
Possible causes:

Incorrect selector.

Element not yet visible.

Page structure changed.

A consent or verification page appeared.

Recommended action: Inspect the current page and use a stable, appropriate locator with a meaningful wait.

Add to Cart is missing or disabled
Possible causes:

Product unavailable.

A variation must be selected.

Page is still loading.

Current session exposes a different layout.

Recommended action: Inspect the availability message and record the observed state. Skip dependent steps only when the prerequisite is genuinely unavailable.

API and UI values do not match
Possible causes:

Different data sources.

Different currency or formatting.

Product variation mismatch.

Price changes or stale reference data.

Recommended action: Verify that both sources refer to the same product and field before applying justified normalization.

Authentication state is missing or expired
Possible causes:

Setup script was not run.

State file was moved or deleted.

Session was revoked or expired.

The application uses additional session mechanisms.

Recommended action: Check the file path, validate the authenticated indicator, and repeat authorized authentication when necessary.

GitHub push is rejected
Possible causes:

Authentication failed.

Remote repository contains commits not present locally.

Incorrect remote URL or branch configuration.

Recommended action: Verify the remote and branch, authenticate using an approved GitHub method, and integrate remote changes safely before pushing.

12. Git and GitHub Workflow
Before committing, check the project status:

git status
Stage the project files:

git add README.md requirements.txt .gitignore
git add tests/ configuration/ test_data/ utilities/
git add conftest.py pytest.ini
Adjust the paths to match the files that actually exist.

Commit the changes:

git commit -m "Add Playwright automation assignment"
Push the committed code:

git push
If the local branch does not have an upstream configured, use the appropriate remote and branch, for example:

git push -u origin main
Before pushing, verify that no authentication state, credentials, or sensitive test artifacts are staged.

13. Acceptance Criteria
The project is ready for review when the implemented tasks meet the following criteria:


Product search and detail-page validation work as expected.


Products are selected using visible titles or stable identifiers.


Locators are robust and appropriately scoped.


Autocomplete and fallback search behavior are handled.


Cart validation stops before purchase.


API/UI comparison uses an approved reference source.


Product identity is checked across navigation.


Pagination or scrolling behavior is recorded accurately.


Form persistence is tested using safe test data.


Conditional execution includes clear reasons.


Authorized browser state is saved and reused successfully.


Missing and expired session scenarios are handled.


Test results and failure evidence are generated.


Sensitive state files are excluded from Git and submission.


README documentation reflects the actual implementation.

These acceptance criteria should be checked against the tests that have actually been implemented and executed. A checklist item is not evidence of a passing test by itself.

14. Future Enhancements
Possible improvements include:

Page Object Model for separating locators and page actions from test logic.

Parameterized tests for multiple trainer-approved search keywords.

Improved test-data management.

Structured logging.

More detailed API validation.

Additional failure diagnostics.

Continuous integration using an authorized test environment.

Browser and viewport coverage.

Consistent test tagging and selective execution.

Any future enhancement should preserve test isolation, meaningful assertions, and the security requirements for authenticated sessions.

15. Conclusion
This project provides a practical foundation for learning end-to-end browser automation using Python, Playwright, and Pytest.

It demonstrates how to identify products dynamically, interact with changing web interfaces, validate application state, handle conditional workflows, compare trusted data sources, and reuse

Final checklist before submitting to Git



⋮⋮⋮⋮⋮⋮⋮⋮
