---
name: playwright-python
description: Playwright Python Best Practices and Techniques (Sync/Async, POM, Locators)
---

# Playwright Python Best Practices & Techniques

Playwright for Python is a powerful library for browser automation, web scraping, and end-to-end testing. It provides both Sync and Async APIs, auto-waiting, and resilient locators.

## 1. Testing Philosophy
- **Test User-Visible Behavior:** Interact with the rendered output (what the user sees), not the implementation details (CSS classes or XPath).
- **Isolation:** Each test should run independently. Use `pytest-playwright` fixtures (`page`, `context`) which automatically create a fresh browser context and page for each test.
- **Avoid Third-Party Dependencies:** Mock network requests to external APIs using Playwright's network routing (`page.route`).

## 2. Locators & Auto-Waiting
Playwright locators come with **auto-waiting** and **retry-ability**. They wait for elements to become actionable (visible, enabled, stable) before performing actions. Do not use `time.sleep()`.

**👍 Best Practice (Resilient):**
```python
# Use user-facing attributes
page.get_by_role("button", name="Submit").click()
page.get_by_label("Username").fill("admin")
page.get_by_placeholder("Search...").fill("Playwright")
page.get_by_text("Welcome back").click()
```

**👎 Bad Practice (Brittle):**
```python
# Breaks easily if the designer changes the class or DOM structure
page.locator("button.buttonIcon.submit-btn").click()
page.locator("//*[@id='login']/div[1]/button").click()
```

## 3. Web-First Assertions
Use `expect` from `playwright.sync_api` (or `async_api`). These assertions automatically wait and retry until the condition is met.

```python
from playwright.sync_api import expect

# 👍 Good: Waits and retries until the element is visible
expect(page.get_by_text("welcome")).to_be_visible()

# 👎 Bad: Checks instantly and fails if the element hasn't loaded yet
assert page.get_by_text("welcome").is_visible()
```

## 4. Page Object Model (POM)
POM encapsulates page structure and operations into classes, making tests maintainable and reusable.

**Implementation (models/login_page.py):**
```python
from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_label("Username")
        self.password_input = page.get_by_label("Password")
        self.submit_button = page.get_by_role("button", name="Sign in")

    def goto(self):
        self.page.goto("https://example.com/login")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.submit_button.click()
```

**Usage in Test (test_login.py):**
```python
from models.login_page import LoginPage
from playwright.sync_api import expect

def test_valid_login(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("user1", "pass123")
    
    expect(page.get_by_text("Dashboard")).to_be_visible()
```

## 5. Async API Integration
If you are scraping or integrating with async frameworks (like FastAPI), use the `async_api`.

```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://playwright.dev/")
        print(await page.title())
        await browser.close()

asyncio.run(main())
```

## 6. Tracing and Debugging
- **Trace generation in Pytest:** Run `pytest --tracing=retain-on-failure`
- **View traces:** `playwright show-trace trace.zip`
- **Codegen:** Use `playwright codegen <url>` to record interactions and auto-generate resilient Python code and locators.