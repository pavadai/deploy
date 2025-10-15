import streamlit as st
import pandas as pd
import cv2
from PIL import Image
import numpy as np
# Load color dataset
csv_file = 'colors.csv'
df = pd.read_csv(csv_file)
def get_color_name(R, G, B):
minimum = float('inf')
cname = ""
for i in range(len(df)):
d = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B -
int(df.loc[i, "B"]))
if d < minimum:
minimum = d
cname = df.loc[i, "color_name"]
return cname
st.title("Color Detection Application")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg",
"jpeg", "png"])
if uploaded_file is not None:
image = Image.open(uploaded_file)
img_array = np.array(image)
st.image(image, caption='https://sl.bing.net/eHC5txea0Fo',
use_column_width=True)
st.write("Click on the image to detect the color.")
coords = st.experimental_data_editor({"x": [], "y": []}, num_rows=1)
if not coords.empty:
x = coords.iloc[0]['x']
y = coords.iloc[0]['y']
if 0 <= y < img_array.shape[0] and 0 <= x < img_array.shape[1]:
pixel = img_array[y, x]
R = pixel[0]
G = pixel[1]
B = pixel[2]
cname = get_color_name(R, G, B)
st.write(f"**Color Name:** {cname}")
st.write(f"**RGB Values:** {R}, {G}, {B}")
st.markdown(f"<div
style='width:100px;height:100px;backgroundcolor:
rgb({R},{G},{B});'></div>", unsafe_allow_html=True)
else:
st.error("Click coordinates out of image bounds.")
7.Challenges
