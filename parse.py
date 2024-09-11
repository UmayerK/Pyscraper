import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

# Load environment variables
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def query_openai(prompt, content):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts specific information from given text content."},
                {"role": "user", "content": f"Content: {content}\n\nTask: {prompt}"}
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error connecting to OpenAI API: {str(e)}")
        return None

def parse_content(content_chunks, question):
    template = (
        "You are tasked with extracting specific information from the following text content. "
        "Please follow these instructions carefully:\n\n"
        "1. Extract Information: Only extract the information that directly matches the provided description.\n"
        "2. No Extra Content: Do not include any additional text, comments, or explanations in your response.\n"
        "3. Empty Response: If no information matches the description, return an empty string ('').\n"
        "4. Direct Data Only: Your output should contain only the data that is explicitly requested, with no other text.\n\n"
        "Description: {parse_description}"
    )
    
    results = []
    for chunk in content_chunks:
        prompt = template.format(parse_description=question)
        result = query_openai(prompt, chunk)
        if result and result.strip():  # Only add non-empty results
            results.append(result)
    
    return "\n".join(results)
