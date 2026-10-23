# Scrappy (Pyscraper)

A small Streamlit app that answers questions about a web page. You give it a URL and a question; it loads the page through a remote Selenium browser, strips the HTML down to readable text, and asks an OpenAI model to pull out only the information you asked for.

## How it works

1. **Scrape** (`scraper.py`) – connects to a remote Chromium session (Bright Data Scraping Browser) with Selenium, opens the URL, waits for the page/CAPTCHA, saves a screenshot to `page.png`, and returns the page HTML.
2. **Clean** (`main.py`) – BeautifulSoup extracts the `<body>`, removes `<script>`/`<style>`, and collapses the text; it is split into 4,000-character chunks.
3. **Extract** (`parse.py`) – each chunk is sent to `gpt-3.5-turbo` with a strict "return only the matching data" prompt; non-empty answers are joined.
4. **UI** – a Streamlit page with a sidebar of chats. Each chat keeps its URL, question, answer, raw HTML and cleaned text in session state.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file (it is git-ignored):

```
OPENAI_API_KEY=sk-...
SBR_WEBDRIVER=https://<user>:<password>@brd.superproxy.io:9515
```

`SBR_WEBDRIVER` is the WebDriver endpoint of a Bright Data Scraping Browser zone. Export it in your shell if you are not loading `.env` for `scraper.py`.

## Run

```bash
streamlit run main.py
```

## Tech

Python, Streamlit, Selenium (remote WebDriver), BeautifulSoup, OpenAI API, python-dotenv.
