# app.py
from PIL import Image, ImageOps
import streamlit as st
from io import BytesIO


# Convert Pillow image to byte data for Streamlit
def pillow_to_streamlit(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return buffered.getvalue()

# Streamlit app
st.set_page_config("Mask enhancer", layout="wide")
_, window, _ = st.columns([0.1, 0.5, 0.1])

window.title("Simple mask enhancer")
window.write("Works by converting an image to greyscale and then making a simple check")
window.code('''
            if pixel_value > threshold
                pixel_value = white
            else
                pixel_value = black
            ''')
window.write("You can inverse the check with Inverse Threshold checkbox")

uploaded_file = window.file_uploader("Choose an image...", type=["png", "jpg"])

if uploaded_file is not None:

    col1, col2, col3, col4, col5 = window.columns([0.2, 0.2, 0.2, 0.2, 0.2])

    # Convert Pillow image to byte format and display in Streamlit
    col1.image(uploaded_file, use_column_width=True, caption="Original image")

    with Image.open(uploaded_file) as image:
        image.convert('RGBA')

        threshold = window.slider("Threshold", 0, 255, value = 3)
        inverse = window.checkbox("Inverse Threshold?")

        grayscale_image = ImageOps.grayscale(image)
        processed_image = grayscale_image.point(lambda p: 255 if p > threshold else 0) if not inverse else grayscale_image.point(lambda p: 255 if p < threshold else 0)
        
        alpha_image = Image.new('L', size=image.size)
        alpha_image.putalpha(processed_image)

  

        col2.image(pillow_to_streamlit(grayscale_image), use_column_width=True)
        col3.image(pillow_to_streamlit(processed_image), use_column_width=True)
        col4.image(pillow_to_streamlit(alpha_image), use_column_width=True)

        filename = uploaded_file.name.split('.')[0]
        col2.download_button("Download greyscale", pillow_to_streamlit(grayscale_image), file_name = f'{filename}_greyscale.png', use_container_width = True)
        col3.download_button("Download alpha inversed", pillow_to_streamlit(processed_image), file_name = f'{filename}_processed.png', use_container_width = True)
        col4.download_button("Download alpha mask", pillow_to_streamlit(alpha_image), file_name = f'{filename}_mask.png', use_container_width = True)

        image.putalpha(processed_image)
        col5.image( image, use_column_width=True )
        col5.download_button("Download masked image", pillow_to_streamlit(image), file_name = f'{filename}_masked.png', use_container_width = True)

    
    
