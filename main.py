import os
import sys
import streamlit as st

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import the functions from scraper
from scraper import is_valid_url, scrape_website

# Print current directory and its contents for debugging
print("Current working directory:", os.getcwd())
print("Files in the current directory:", os.listdir())

# Set page configuration
st.set_page_config(page_title="Scrappy", page_icon="🔍", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-color: #222222;
    }
    .stButton>button {
        background-color: purple;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("Welcome to Scrappy")

# URL input field
url = st.text_input("Enter URL:", placeholder="https://example.com")

# Submit button
if st.button("Submit"):
    if url:
        if not is_valid_url(url):
            st.error(f"Invalid URL: {url}. Please enter a valid URL including the protocol (e.g., https://)")
        else:
            with st.spinner("Scraping..."):
                log, result = scrape_website(url)
            
            st.subheader("Scraping Log")
            st.text(log)
            
            if result is None:
                st.error("Scraping failed. Check the log for details.")
            else:
                st.success("Scraping completed!")
                st.subheader("HTML Content")
                st.code(result, language="html")
                
                # Display the screenshot
                st.subheader("Page Screenshot")
                st.image("page.png")
    else:
        st.warning("Please enter a URL before submitting.")
