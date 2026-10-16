
import os
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = os.getenv(
    "BASE_URL",
    "http://localhost:18080"
)


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(3)

    yield browser

    browser.quit()


def test_home_page_loads(driver):
    driver.get(BASE_URL)

    assert driver.title.strip() != ""
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_dashboard_response(driver):
    driver.get(BASE_URL)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "body"))
    )

    assert driver.current_url.startswith(BASE_URL)



def test_student_page_navigation(driver):
    driver.get(BASE_URL)

    links = driver.find_elements(By.TAG_NAME, "a")
    student_links = [
        link for link in links
        if "student" in link.text.lower()
    ]

    if not student_links:
        pytest.skip("No student navigation link found.")

    student_links[0].click()

    WebDriverWait(driver, 10).until(
        lambda browser: browser.current_url != BASE_URL
    )

    assert driver.current_url != BASE_URL
