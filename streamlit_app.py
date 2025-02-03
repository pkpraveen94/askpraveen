import streamlit as st
import requests
from gtts import gTTS
import os

# API URL
url = "https://2owawgyt71.execute-api.us-east-1.amazonaws.com/dev/blog-generation"

# App Title
st.set_page_config(page_title="Ask Praveen", layout="centered", page_icon="🙏")
st.title("🙏 Ask Praveen")

# Background and Styling
st.markdown(
    """
    <style>
        html, body, [class*="css"] {
            background-color: white !important;
            color: black !important;
            font-family: Arial, sans-serif;
        }
        .stTextInput input {
            background-color: #f9f9f9;
            color: black;
            border: 1px solid #ccc;
        }
        .stButton button {
            background-color: #007bff;
            color: white !important;
            font-weight: bold;
            border-radius: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Introduction section
st.markdown(""" 
### Welcome to Ask Praveen
🙏 Ask your Questions and you will get responses in couple of sentences Only!.
""")

# Input section
question = st.text_input("What type of Question is on your mind today?")

# Variable to store answer status
guidance_answer = None

# Submit button for asking question
if st.button("Ask Praveen"):
    if question:
        try:
            # Send the question directly without modifying the prompt
            response = requests.post(url, json={"blog_topic": question})
            
            if response.status_code == 200:
                data = response.json()

                # Extract the 'places_content' from the response
                guidance_answer = data.get("places_content", None)
                
                if guidance_answer:
                    st.success("Here's the Response Praveen Gave for you:")
                    st.write(guidance_answer)
                else:
                    st.warning("No Reponse found for your question by Praveen!")
            else:
                st.error(f"Failed to retrieve guidance. Server responded with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while making the request: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter a question before asking Praveen.")

# Only show the "Hear the Guidance" button if there's an answer
if guidance_answer:
    if st.button("🎧 Hear the Guidance"):
        # Convert text to speech (voice note)
        tts = gTTS(text=guidance_answer, lang='en')
        tts.save("answer.mp3")
        
        # Play the voice note
        st.audio("answer.mp3")
        
        # Optionally delete the audio file after use
        os.remove("answer.mp3")

# Footer with two-hand worship symbol
st.markdown(""" 
---
<div style="text-align: center;">
    🙌 Powered by Ask Praveen 🙌
</div>
""", unsafe_allow_html=True)
