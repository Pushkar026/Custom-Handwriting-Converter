import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")

FONT_MAP = {
    "handwriting": os.path.join(FONTS_DIR, "handwriting.ttf"),
    "calibri": os.path.join(FONTS_DIR, "calibri.ttf"),
    "arial": os.path.join(FONTS_DIR, "arial.ttf"),
    "palscript": os.path.join(FONTS_DIR, "palscript.ttf"),
    "chiller": os.path.join(FONTS_DIR, "chiller.ttf"),
    "rage": os.path.join(FONTS_DIR, "rage.ttf"),
}
