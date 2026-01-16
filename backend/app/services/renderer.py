from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap


def render_handwritten_text(
    text: str,
    output_path: Path,
    font_path: Path,
    background_path: Path,
    font_size: int = 34,
    left_margin: int = 140,   # after red margin
    top_margin: int = 120,
    line_gap: int = 72,       # distance between ruled lines (match image)
):
    # ---------- SAFETY ----------
    if not font_path.exists():
        raise FileNotFoundError(f"Font not found: {font_path}")

    if not background_path.exists():
        raise FileNotFoundError(f"Background not found: {background_path}")

    font = ImageFont.truetype(str(font_path), font_size)

    # ---------- LOAD BACKGROUND ----------
    bg = Image.open(background_path).convert("RGB")
    img = bg.copy()
    draw = ImageDraw.Draw(img)

    # ---------- WORD WRAPPING ----------
    max_width = img.width - left_margin - 80
    wrapped_lines = []

    for line in text.split("\n"):
        words = line.split(" ")
        current = ""

        for word in words:
            test = current + word + " "
            if font.getlength(test) <= max_width:
                current = test
            else:
                wrapped_lines.append(current.strip())
                current = word + " "
        wrapped_lines.append(current.strip())

    # ---------- DRAW TEXT ----------
    y = top_margin

    for line in wrapped_lines:
        draw.text(
            (left_margin, y),
            line,
            fill=(30, 30, 30),  # clean ink
            font=font,
        )
        y += line_gap

        if y > img.height - 100:
            break  # prevent overflow (later → pagination)

    img.save(output_path)
