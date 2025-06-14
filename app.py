# app.py

import streamlit as st
from PIL import Image
from io import BytesIO
import requests

from utils.gemini_api import identify_plant, plant_care_tips

st.set_page_config(
    page_title="Plant Pal • AI Plant Care",
    layout="wide",
    page_icon="🌿"
)

# --- Sidebar: Dynamic Logo & Info ---
with st.sidebar:
    st.markdown("### 🌿 Plant Pal")
    logo_file = st.file_uploader("Upload your Plant Pal logo (optional)", type=["png", "jpg", "jpeg"], key="logo_upload")
    if logo_file:
        st.image(logo_file, width=120)
    else:
        # Show a plant icon if no logo is uploaded
        icon_url = "https://cdn-icons-png.flaticon.com/512/2909/2909831.png"
        img = Image.open(requests.get(icon_url, stream=True).raw)
        st.image(img, width=80)
    st.markdown(
        """
        **Your AI-powered green companion!**
        - Identify any plant  
        - Get care tips instantly  
        - More features coming soon!
        """
    )
    st.markdown("---")
    st.markdown("**How it works:**\n1. Upload a plant photo\n2. Get instant results!\n")
    st.info("Built with ❤️ using Google Gemini & Streamlit.")

# --- Main Area: Welcome & Upload ---
st.markdown(
    "<h1 style='text-align: center; color: #356859;'>🌱 Welcome to Plant Pal</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<div style='text-align: center;'>Snap or upload a photo of any plant to get instant care advice and fun facts!</div>",
    unsafe_allow_html=True
)
st.markdown("---")

st.markdown("### 📸 Upload Plant Image", unsafe_allow_html=True)
upload_col, spacer, preview_col = st.columns([2, 0.2, 2])

with upload_col:
    uploaded_file = st.file_uploader(
        "",
        type=["jpg", "jpeg", "png"],
        key="plant_upload"
    )

if uploaded_file:
    image_bytes = uploaded_file.getvalue()
    image = Image.open(BytesIO(image_bytes))
    with preview_col:
        st.image(image, caption="Your Uploaded Plant", use_column_width=True, output_format="PNG")

    st.markdown("---")

    with st.spinner("🔎 Identifying your plant..."):
        plant_info = identify_plant(image_bytes)

    if plant_info.startswith("❌ Error"):
        st.error(plant_info)
    else:
        lines = [line for line in plant_info.split("\n") if line.strip()]
        plant_name = lines[0] if lines else "Unknown Plant"

        st.markdown("### 🌿 Identification & Facts")
        st.success("\n".join(lines))

        with st.spinner("🌤️ Fetching care instructions..."):
            care_details = plant_care_tips(plant_name)
        if care_details.startswith("❌ Error"):
            st.error(care_details)
        else:
            st.markdown("### 🛠️ Care Instructions")
            st.info(care_details)
else:
    st.info("⬆️ **Let's grow together! Upload a clear photo of a plant to get started.**")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #A3A847;'>Plant Pal &copy; 2025 • Open Source 🌿</div>",
    unsafe_allow_html=True
)
