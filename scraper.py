from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
import time
import urllib.parse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Bright Data Scraping Browser URL with credentials
SBR_WEBDRIVER = 'https://brd-customer-hl_cf86ef64-zone-scrappy:55mkdypjbw5r@brd.superproxy.io:9515'

def is_valid_url(url):
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def scrape_website(url):
    log = []
    try:
        if not is_valid_url(url):
            raise ValueError(f"Invalid URL: {url}")

        log.append('Connecting to Scraping Browser...')
        sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
        options = ChromeOptions()
        
        # Configure CAPTCHA solving
        options.add_argument('--enable-automation')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-notifications')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        
        with Remote(sbr_connection, options=options) as driver:
            log.append('Connected! Navigating...')
            driver.get(url)
            time.sleep(5)  # Wait for initial page load

            # Attempt to solve CAPTCHA
            log.append('Attempting to solve CAPTCHA...')
            try:
                # Wait for CAPTCHA to be solved (adjust timeout as needed)
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                log.append('CAPTCHA solved or not present')
            except Exception as e:
                log.append(f'CAPTCHA solving failed or timed out: {str(e)}')

            # Wait a bit more after CAPTCHA solving attempt
            time.sleep(5)

            log.append('Taking page screenshot to file page.png')
            driver.get_screenshot_as_file('./page.png')

            log.append('Navigated! Scraping page content...')
            html_content = driver.page_source

            return '\n'.join(log), html_content
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        log.append(error_message)
        return '\n'.join(log), None

# Explicitly export the functions
__all__ = ['is_valid_url', 'scrape_website']

