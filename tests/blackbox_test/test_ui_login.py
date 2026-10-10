import pytest
from playwright.sync_api import expect

from src.pages.login_page import LoginPage

pytestmark = pytest.mark.ui

@pytest.fixture
def page_client(page):
    USERNAME = "standard_user"
    PASSWORD = "secret_sauce"
    URL = "https://www.saucedemo.com/"

    client = LoginPage(URL, USERNAME, PASSWORD)
    client.login(page)

    return page

def test_login_success(page_client):
    expect(page_client).to_have_url("https://www.saucedemo.com/inventory.html")

    title = page_client.locator("span.title")
    expect(title).to_have_text("Products")
    expect(title).to_be_visible()