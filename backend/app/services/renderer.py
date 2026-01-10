from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def render_handwritten_text(
    text: str,
    output_path: Path,
    font_path: Path,
    image_width: int = 800,
    margin: int = 50,
    font_size: int = 32,
    line_spacing: int = 10,
):
   

    font = ImageFont.truetype(str(font_path), font_size)

    temp_img = Image.new("RGB", (image_width, 1000), "white")
    temp_draw = ImageDraw.Draw(temp_img)

    lines = text.split("\n")
    line_height = font_size + line_spacing
    image_height = margin * 2 + len(lines) * line_height

    img = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(img)

    y = margin
    for line in lines:
        draw.text((margin, y), line, fill="black", font=font)
        y += line_height

    img.save(output_path)
