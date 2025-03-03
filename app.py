# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 17:33:21 2024

@author: chaki
"""
  

import streamlit as st
import os
from mistralai import Mistral


def generate_response(input_text, img_url):
    global client
    model = 'pixtral-large-latest'
    chat_response = client.chat.complete(
        model=model, 
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": input_text},  # Use the actual input_text
                {"type": "image_url", "image_url": img_url}
            ]
        }]
    )
    return chat_response.choices[0].message.content


st.title("🏠🔗 Use Case 03: Vision LLm ")

st.write(""" 
         chat over an image. Powered by Pixtral Vision LLm by Mistral. No OCR is applied. Amazing!
         """)

mistral_api_key = st.sidebar.text_input("Mistral API Key", type="password")

# Default images to display

image_urls = {
    "Algiers at night":"https://i0.wp.com/www.dzair-tube.dz/en/wp-content/uploads/2024/04/Algerias-Capital-Embarks-on-Urban-Renaissance-Minister-Merad-Oversees-Ambitious-Projects-for-a-Modern-Metropolis-1-jpg.webp?fit=1024%2C576&ssl=1",
    "Official Pixtral Perfs":"https://mistral.ai/images/news/pixtral-large/pixtral-large-header-fig.png",
    "Dijsktra Algorithm":"https://www.adamk.org/wp-content/uploads/2019/04/whiteboard-dijkstra.jpg"
}

# Display the default images with captions
st.subheader("Select a default image to analyze:")

img_items = list(image_urls.items())

cols = st.columns(len(img_items))

# Initialize session state for selected image
if 'selected_image_url' not in st.session_state:
    st.session_state.selected_image_url = None
if 'selected_caption' not in st.session_state:
    st.session_state.selected_caption = None

# Modify the button click handlers
for i, (caption, url) in enumerate(img_items):
    with cols[i]:
        st.image(url, caption=caption)
        if st.button(f"Select {caption}"):
            st.session_state.selected_image_url = url
            st.session_state.selected_caption = caption

# Update the display of selected image
if st.session_state.selected_image_url:
    st.write(f"chat over The image representing: {st.session_state.selected_caption}")

# Update the form section
with st.form("my_form"):
    text = st.text_area(
        "Message the System:",
        "Describe what you see in this image",
        key="user_input"
    )
    submitted = st.form_submit_button("Submit")

    if submitted:
        if not mistral_api_key:
            st.warning("Please enter your Mistral API key!", icon="⚠")
        elif not st.session_state.selected_image_url:
            st.warning("Please select an image to analyze!", icon="⚠")
        else:
            client = Mistral(api_key=mistral_api_key)
            st.info("Processing the image...")
            try:
                response = generate_response(text, st.session_state.selected_image_url)
                st.write(response)
            except Exception as e:
                st.error(f"Error processing request: {str(e)}")
