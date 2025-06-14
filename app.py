# app.py

import streamlit as st
from PIL import Image
from utils.gemini_api import identify_plant, plant_care_tips

st.set_page_config(
    page_title="PlantCare AI",
    layout="centered",
    page_icon="🌱"
)

st.title("🌱 PlantCare AI")
st.markdown("**Upload a plant photo to identify its species and get personalized care instructions!**")

uploaded_file = st.file_uploader(
    "📸 Upload Plant Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    try:
        image_bytes = uploaded_file.getvalue()
        from io import BytesIO
        image = Image.open(BytesIO(image_bytes))
        st.image(image, caption="Your Uploaded Plant", use_column_width=True)
        
        with st.spinner("🔎 Identifying your plant..."):
            plant_info = identify_plant(image_bytes)
        
        # ...rest of your code unchanged...

        
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
    except Exception as e:
        st.error(f"File error: {e}")
else:
    st.info("⬆️ **Upload a clear photo of a plant to get started.**")
