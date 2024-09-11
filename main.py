import os
import sys
import streamlit as st
from bs4 import BeautifulSoup
import requests
import traceback

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import the functions from scraper and parse
from scraper import is_valid_url, scrape_website
try:
    from parse import parse_content
except ImportError:
    st.error("Unable to import parse_content. Make sure parse.py is in the same directory as main.py.")
    parse_content = None

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    body = soup.find('body')
    return body.decode_contents() if body else ''

def clean_content(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')
    
    # Remove script and style elements
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()
    
    # Get text and separate with newlines
    cleaned_text = soup.get_text(separator='\n')
    
    # Remove empty lines and strip whitespace
    cleaned_content = '\n'.join(line.strip() for line in cleaned_text.split('\n') if line.strip())
    
    return cleaned_content

def split_content(dom_content, max_length=4000):  # Reduced max_length to fit within OpenAI's token limit
    return [dom_content[i:i+max_length] for i in range(0, len(dom_content), max_length)]

# Set page configuration
st.set_page_config(page_title="Scrappy", page_icon="🔍", layout="wide")

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

# Description/Question input field
user_question = st.text_area("What do you want to know about the content?", height=100)

# Submit button
if st.button("Submit"):
    if url and user_question:
        if not is_valid_url(url):
            st.error(f"Invalid URL: {url}. Please enter a valid URL including the protocol (e.g., https://)")
        else:
            with st.spinner("Scraping and processing..."):
                log, result = scrape_website(url)
            
            st.subheader("Scraping Log")
            st.text(log)
            
            if result is None:
                st.error("Scraping failed. Check the log for details.")
            else:
                st.success("Scraping completed!")
                
                # Original HTML content in an expander
                with st.expander("Original HTML Content"):
                    st.code(result, language="html")
                
                # Extract and clean content
                body_content = extract_body_content(result)
                cleaned_content = clean_content(body_content)
                
                # Cleaned content in an expander
                with st.expander("Cleaned Content"):
                    st.text_area("Cleaned Text", cleaned_content, height=300)
                
                # Split content into batches
                dom_chunks = split_content(cleaned_content)
                
                # Screenshot in an expander
                with st.expander("Page Screenshot"):
                    st.image("page.png")
                
                # Process the question
                try:
                    with st.spinner("Processing your question..."):
                        parsed_answer = parse_content(dom_chunks, user_question)
                    if parsed_answer:
                        st.subheader("Parsed Answer")
                        st.write(parsed_answer)
                    else:
                        st.warning("No relevant information found.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.error(traceback.format_exc())
    elif not url:
        st.warning("Please enter a URL before submitting.")
    elif not user_question:
        st.warning("Please enter a question before submitting.")
