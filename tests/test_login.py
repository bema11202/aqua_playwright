import pytest
from assertpy import assert_that
from playwright.sync_api import sync_playwright
import os
import json
import requests
import jupyter_client


@pytest.fixture(scope="module")
def browser():
    """Launch the browser before the test module."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield browser
        page.close()
        browser.close()


def test_login(browser):
    """Test login with valid credentials."""
    page = browser.new_page()
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    assert_that(page.url).contains("inventory.html")


def test_login_invalid_password(browser):
    """Test login with invalid credentials."""
    page = browser.new_page()
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "erfftee")
    page.click("#login-button")
    assert_that((page.locator("h3[data-test='error']")).inner_text()).is_equal_to(
        "Epic sadface: Username and password do not match any user in this service")


def test_login_empty_credentials(browser):
    """Test login with empty credentials."""
    page = browser.new_page()
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "")
    page.fill("#password", "")
    page.click("#login-button")
    assert_that(page.content()).contains("Epic sadface: Username is required")


def test_login_invalid_username(browser):
    """Test login with invalid credentials."""
    page = browser.new_page()
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "invalid_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    assert_that(page.content()).contains("Epic sadface: Username and password do not match any user in this service")


def test_add_to_cart(browser):
    """Test add to cart."""
    page = browser.new_page()
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    page.click("#add-to-cart-sauce-labs-backpack")
    assert_that(page.locator("span[class='shopping_cart_badge']").inner_text()).contains("1")
    assert_that(page.locator("span[class='shopping_cart_badge']").all_inner_texts()).is_not_empty()
    print((page.locator("span[class='shopping_cart_badge']")).all_inner_texts())
    assert_that(page.content()).contains("Sauce Labs Backpack")


def test_remove_from_cart(browser):
    """Test remove from cart."""
    page = browser.new_page()
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    page.click("#add-to-cart-sauce-labs-backpack")
    page.click("#remove-sauce-labs-backpack")
    assert_that((page.locator("span[class='shopping_cart_badge']")).all_inner_texts()).is_empty()
    print((page.locator("span[class='shopping_cart_badge']")).all_inner_texts())
    page.close()
