import streamlit as st
import requests
from io import BytesIO
from PIL import Image

# Hugging Face API token
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
        return None
    elif response.status_code == 200:
        return response.content
    else:
        st.error(f"Failed to generate the image. Response: {response.text}")
        return None

# Custom CSS for stylish fonts and buttons
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    * {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background-color: #101820FF;
        background-image: url("https://brainpod.ai/wp-content/uploads/2024/05/290973-1280x731.png");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }

    h1 {
        color: #32CD32;
        text-shadow: 2px 2px 4px #000;
        font-size: 2.5rem;
        margin-bottom: 30px;
        text-align: center;
    }

    .prompt-box {
        width: 80%;
        margin: 0 auto;
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }

    .generated-image img {
        border-radius: 10px;
        margin: 20px;
    }

    .stTextInput > div > div > input {
        font-size: 1rem;
        padding: 10px;
        border: 2px solid #32CD32;
        border-radius: 10px;
        background-color: rgba(0, 0, 0, 0.05);
        color: #fff;
    }

    .stButton button {
        font-size: 1rem;
        padding: 12px 24px;
        background-color: #32CD32;
        color: white;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .stButton button:hover {
        background-color: #28a745;
    }

    .stTextInput input::placeholder {
        color: #aaaaaa;
        font-style: italic;
    }
    
    </style>
    """, unsafe_allow_html=True)

# Page title and layout
st.title("Text to Image Generator")

# Prompt input
prompt = st.text_input("Enter a text prompt to generate an image:")

# Generate button
if st.button("Generate"):
    if prompt:
        image_bytes = query_huggingface_api(prompt)
        
        if image_bytes:
            # Display the generated image
            image = Image.open(BytesIO(image_bytes))
            st.image(image, caption="Generated Image", use_column_width=True)
    else:
        st.warning("Please enter a prompt to generate an image.")

