import time
import streamlit as st
import requests
from io import BytesIO
from PIL import Image

token = "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"

def query_huggingface_api(prompt):
    headers = {
        "Authorization": f"Bearer {token}",
    }
    api_url = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
    data = {"inputs": prompt}

    response = requests.post(api_url, headers=headers, json=data)
    
    if response.status_code == 503:
        st.warning("Model is still loading, please wait.")
        time.sleep(60) 
        return query_huggingface_api(prompt)  
    elif response.status_code == 200:
        return response.content
    else:
        st.error(f"Failed to generate the image. Response: {response.text}")
        return None

# Streamlit app interface
st.title("Text 2 Image Generator")

# User input text box for prompt
prompt = st.text_input("Create an image from text prompt:")

# Generate button
if st.button("Generate"):
    if prompt:
        # Query the Hugging Face API with the user prompt
        image_bytes = query_huggingface_api(prompt)
        
        if image_bytes:
            image = Image.open(BytesIO(image_bytes))
            st.image(image, caption="Generated Image", use_column_width=True)
    else:
        st.warning("Please enter a prompt to generate an image.")
