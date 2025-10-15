import streamlit as st
import pandas as pd
import cv2
from PIL import Image
import numpy as np

# ---- Load color dataset ----
# Make sure a file named 'colors.csv' is in the same folder.
# It should have columns: color_name,R,G,B
csv_file = 'colors.csv'
df = pd.read_csv(csv_file)

# ---- Function to get nearest color name ----
def get_color_name(R, G, B):
    minimum = float('inf')
    cname = ""
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
        if d < minimum:
            minimum = d
            cname = df.loc[i, "color_name"]
    return cname

# ---- Streamlit App Title ----
st.title("🎨 Color Detection from Image")

# ---- Upload image ----
uploaded_file = st.file_uploader("📤 Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read and display image
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    st.image(image, caption="📷 Uploaded Image", use_column_width=True)

    st.write("👉 Click on the image below to detect the color at that point:")

    # Get click coordinates from Streamlit's image click input
    clicked_point = st.image(image, caption="Click to detect color", use_container_width=True)

    # Streamlit doesn't support click events on images directly yet.
    # So, we simulate this using editable coordinates input.
    st.write("🔢 Enter coordinates (x, y) manually to detect color:")
    coords = st.experimental_data_editor(pd.DataFrame({"x": [0], "y": [0]}), num_rows=1)

    if not coords.empty:
        x = int(coords.iloc[0]['x'])
        y = int(coords.iloc[0]['y'])

        # Check if coordinates are within image bounds
        if 0 <= y < img_array.shape[0] and 0 <= x < img_array.shape[1]:
            pixel = img_array[y, x]
            R, G, B = int(pixel[0]), int(pixel[1]), int(pixel[2])
            color_name = get_color_name(R, G, B)

            # ---- Display results ----
            st.subheader("🎯 Detected Color Info")
            st.write(f"**Color Name:** {color_name}")
            st.write(f"**RGB Values:** ({R}, {G}, {B})")

            st.markdown(
                f"<div style='width:120px;height:120px;background-color:rgb({R},{G},{B});border:2px solid #000;border-radius:10px;'></div>",
                unsafe_allow_html=True
            )
        else:
            st.error("⚠️ Coordinates out of image bounds. Please enter valid (x, y).")

else:
    st.info("👆 Please upload an image to start color detection.")


