

import streamlit as st
import pandas as pd
import cv2
from PIL import Image
import numpy as np

# Load color dataset (make sure colors.csv is in same folder)
csv_file = 'colors.csv'
df = pd.read_csv(csv_file)

# Function to find the nearest color name
def get_color_name(R, G, B):
    minimum = float('inf')
    cname = ""
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
        if d < minimum:
            minimum = d
            cname = df.loc[i, "color_name"]
    return cname

# App Title
st.title("🎨 Color Detection Application")

# Upload Image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the uploaded image
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    # Display image
    st.image(image, caption='https://sl.bing.net/5xLiZXQPAW', use_column_width=True)
    st.write("Enter or edit coordinates (x, y) to detect the color.")

    # Input coordinates using editable table
    coords = st.experimental_data_editor(pd.DataFrame({"x": [0], "y": [0]}), num_rows=1)

    # Process coordinates
    if not coords.empty:
        x = int(coords.iloc[0]['x'])
        y = int(coords.iloc[0]['y'])

        if 0 <= y < img_array.shape[0] and 0 <= x < img_array.shape[1]:
            # Get pixel color
            pixel = img_array[y, x]
            R, G, B = int(pixel[0]), int(pixel[1]), int(pixel[2])
            cname = get_color_name(R, G, B)

            # Display result
            st.write(f"**Color Name:** {cname}")
            st.write(f"**RGB Values:** ({R}, {G}, {B})")

            # Show color box
            st.markdown(
                f"<div style='width:100px;height:100px;background-color:rgb({R},{G},{B});border:1px solid #000;'></div>",
                unsafe_allow_html=True
            )
        else:
            st.error("⚠️ Click coordinates out of image bounds.")
