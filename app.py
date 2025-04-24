import streamlit as st
import os
from PIL import Image
import textwrap

import google.generativeai as genai

# Configure API key
os.environ['GMINI_API_KEY'] = "AIzaSyC1-KxZ89Jdt741SCrvkI79Ut8n5jEv7IE"
genai.configure(api_key=os.environ['GMINI_API_KEY'])

# Helper function to format text as Markdown
def to_markdown(text):
    """Display text as markdown."""
    text = text.replace('*', '  *')
    return textwrap.indent(text, ' >', predicate=lambda _: True)

# Inject CSS for color-changing wavy background with light rainbow colors and styling generated text bold
st.markdown(
    """
    <style>
    @keyframes wave {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    body, .stApp {
        background-image: url('https://png.pngtree.com/thumb_back/fw800/background/20220218/pngtree-dream-background-material-colorful-light-wallpaper-image_964663.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 100vh;
        margin: 0;
        padding: 0;
    }
    .generated-text {
        font-weight: bold !important;
        color: black !important;
        white-space: pre-wrap;
        background-color: rgba(255, 255, 255, 0.7);
        padding: 10px;
        border-radius: 5px;
    }
    .footer-text {
        margin-top: 10px;
        font-weight: bold;
        color: orange;
        text-align: center;
    }
    .deprecation-message {
        font-weight: bold;
        color: white;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit app
st.title("Generative AI Content Generator")

st.markdown('<div class="deprecation-message">Gemini 1.0 Pro Vision has been deprecated on July 12, 2024. Consider switching to different model, for example gemini-1.5-flash.</div>', unsafe_allow_html=True)

st.sidebar.header("Options")

# Model selection
model_name = st.sidebar.selectbox(
    "Select Model",
    [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
)
model = genai.GenerativeModel(model_name)

# Input options
input_type = st.sidebar.radio("Input Type", ["Text Prompt", "Image Upload"])

if input_type == "Text Prompt":
    prompt = st.text_area("Enter your prompt:")
    if st.button("Generate Content"):
        with st.spinner("Generating content..."):
            response = model.generate_content(prompt)
            st.markdown(f'<div class="generated-text">{to_markdown(response.text)}</div>', unsafe_allow_html=True)
            st.markdown('<div class="footer-text">MADE BY RATNAPRAVA MOHAPATRA</div>', unsafe_allow_html=True)
elif input_type == "Image Upload":
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        img = Image.open(uploaded_image)
        st.image(img, caption="Uploaded Image", use_column_width=True)
        if st.button("Generate Content from Image"):
            with st.spinner("Generating content..."):
                response = model.generate_content(img)
                st.markdown(f'<div class="generated-text">{to_markdown(response.text)}</div>', unsafe_allow_html=True)
                st.markdown('<div class="footer-text">MADE BY RATNAPRAVA MOHAPATRA</div>', unsafe_allow_html=True)

# Footer
st.sidebar.info("Powered by Google Generative AI")
