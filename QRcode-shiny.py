import streamlit as st
import qrcode
from PIL import Image
from PIL import ImageDraw
import io
import base64


# Define the main function that creates the QR code
def create_qr_code(link, box_size, border):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# Define the function that changes the style of the QR code
def change_style_qr_code(img, style):
    if style == "none":
        return img
    elif style == "rounded":
        box_size = min(img.size[0], img.size[1]) // (len(img.mode) * 4)
        img = img.convert("RGBA")
        w, h = img.size
        radius = int(box_size * 0.2)
        circle = Image.new('L', (radius * 2, radius * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)
        alpha = Image.new('L', img.size, 255)
        alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
        alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
        alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
        alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))
        img.putalpha(alpha)
        return img
    else:
        return None

# Define the function that changes the main colors of the QR code
def change_colors_qr_code(img, color1, color2, color3):
    img = img.convert("RGBA")
    data = img.getdata()
    newData = []
    for item in data:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append((color1[0], color1[1], color1[2], 255))
        elif item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((color2[0], color2[1], color2[2], 255))
        else:
            newData.append((color3[0], color3[1], color3[2], 255))
        img.putdata(newData)
    return img

# Define the main function that creates the app
def main():
    st.title("QR Code Generator")

    # Get user input for the link
    link = st.text_input("Enter the link:")

    # Get user input for the box size and border
    box_size = st.slider("Box size:", 1, 10, 4)
    border = st.slider("Border size:", 0, 10, 2)

    # Get user input for the style
    style = st.selectbox("Select the style:", ["none", "rounded"])

    # Get user input for the main colors
    color1 = tuple(int(x, 16) for x in st.color_picker("Color 1", "#000000").lstrip('#'))
    color2 = tuple(int(x, 16) for x in st.color_picker("Color 2", "#FFFFFF").lstrip('#'))
    color3 = tuple(int(x, 16) for x in st.color_picker("Color 3", "#FF0000").lstrip('#'))


    # Create the QR code image
    img = create_qr_code(link, box_size, border)

    # Change the style of the QR code image
    img = change_style_qr_code(img, style)

    # Change the main colors of the QR code image
    img = change_colors_qr_code(img, color1, color2, color3)

    # Download the QR code image as a PNG file
    if st.button("Download PNG"):
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        href = f'<a href="data:file/png;base64,{img_str}" download="qr_code.png">Download</a>'
        st.markdown(href, unsafe_allow_html=True)


    # Show the QR code image
    st.image(img, use_column_width=True)

if __name__ == "__main__":
    main()
