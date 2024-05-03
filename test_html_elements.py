from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pytest
import re

@pytest.fixture
def driver():
    # Setup Firefox options
    firefox_options = Options()
    firefox_options.add_argument("--headless")  # Ensures the browser window does not open
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Firefox(options=firefox_options)
    yield driver
    driver.quit()

def test_h1_tag_content(driver):
    driver.get("http://10.48.10.163")

    h1_text = driver.find_element(By.TAG_NAME, "h1").text
    assert "Vite + React" == h1_text, "The <h1> tag does not contain the text 'Vite + React'!'"

@pytest.mark.asyncio
async def test_count_increment(driver):
    driver.get("http://10.48.10.163")

    button = driver.find_element(By.TAG_NAME, "button")
    button_text = button.text

    match = re.search(r'\d+', button_text)

    if match is not None:
        number = int(match.group())
    else:
        raise ValueError("No number found in button text")

    button.click()

    # Wait for the button text to change
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "button"), f"count is {number + 1}")
    )

    new_button_text = button.text
    assert new_button_text == f"count is {number + 1}", "The count did not increment by 1"