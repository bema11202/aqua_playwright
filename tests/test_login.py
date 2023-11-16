import pytest
from assertpy import assert_that
from playwright.sync_api import sync_playwright
import os
import assertpy
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


def test_login(browser):
    """Test login with valid credentials."""
    page = browser.new_page()
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    assertpy.assert_that(page.url).contains("inventory.html")
    page.close()


def test_login_invalid_password(browser):
    """Test login with invalid credentials."""
    page = browser.new_page()
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "<PASSWORD>")
    assertpy.assert_that(page.content()).contains("Epic sadface: Password is required")
    page.close()


def test_login_empty_credentials(browser):
    """Test login with empty credentials."""
    page = browser.new_page()
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "")
    page.fill("#password", "")
    page.click("#login-button")
    assertpy.assert_that(page.content()).contains("Epic sadface: Username is required")
    page.close()


def test_login_invalid_username(browser):
    """Test login with invalid credentials."""
    page = browser.new_page()
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "invalid_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    assertpy.assert_that(page.content()).contains("Epic sadface: Password is required")
    page.close()