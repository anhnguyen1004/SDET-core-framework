import os
import pytest
import requests

from playwright.sync_api import expect

from src.pages.login_page import LoginPage

pytestmark = pytest.mark.smoke

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

def test_staging_server_is_alive():
    base_url = os.getenv("BASE_URL", "http://localhost:3000")
    response = requests.get(f"{base_url}/api/users?page=2")
    assert response.status_code == 200