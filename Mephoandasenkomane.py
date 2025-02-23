import ctypes
import random
from time import sleep
from ctypes import windll, wintypes

# Constants
WHITE_BRUSH = 0
SRCCOPY = 0x00CC0020

# Get the device context for the entire screen
hdc = windll.user32.GetDC(0)

# Screen dimensions
screen_width = windll.user32.GetSystemMetrics(0)
screen_height = windll.user32.GetSystemMetrics(1)

# Define the LOGFONT structure
class LOGFONT(ctypes.Structure):
    _fields_ = [
        ("lfHeight", wintypes.LONG),
        ("lfWidth", wintypes.LONG),
        ("lfEscapement", wintypes.LONG),
        ("lfOrientation", wintypes.LONG),
        ("lfWeight", wintypes.LONG),
        ("lfItalic", wintypes.BYTE),
        ("lfUnderline", wintypes.BYTE),
        ("lfStrikeOut", wintypes.BYTE),
        ("lfCharSet", wintypes.BYTE),
        ("lfOutPrecision", wintypes.BYTE),
        ("lfClipPrecision", wintypes.BYTE),
        ("lfQuality", wintypes.BYTE),
        ("lfPitchAndFamily", wintypes.BYTE),
        ("lfFaceName", wintypes.WCHAR * 32)
    ]

def draw_zoom_effect(hdc):
    zoom_factor = 1.05
    frame_width = int(screen_width / 2)  # Define the width of the frame
    frame_height = int(screen_height / 2)  # Define the height of the frame
    frame_x = (screen_width - frame_width) // 2  # Center the frame horizontally
    frame_y = (screen_height - frame_height) // 2  # Center the frame vertically
    
    memdc = windll.gdi32.CreateCompatibleDC(hdc)
    bitmap = windll.gdi32.CreateCompatibleBitmap(hdc, screen_width, screen_height)
    windll.gdi32.SelectObject(memdc, bitmap)

    windll.gdi32.StretchBlt(memdc, 0, 0, screen_width, screen_height, hdc, frame_x, frame_y, frame_width, frame_height, SRCCOPY)
    windll.gdi32.BitBlt(hdc, 0, 0, screen_width, screen_height, memdc, 0, 0, SRCCOPY)

    windll.gdi32.DeleteObject(bitmap)
    windll.gdi32.DeleteDC(memdc)

def draw_text(hdc, text):
    text_x = random.randint(0, screen_width)
    text_y = random.randint(0, screen_height)

    lf = LOGFONT()
    lf.lfHeight = 80  # Increase the font height for larger text
    hf = windll.gdi32.CreateFontIndirectW(ctypes.byref(lf))
    old_hf = windll.gdi32.SelectObject(hdc, hf)

    color = random.randint(0, 0xFFFFFF)
    windll.gdi32.SetTextColor(hdc, color)
    windll.gdi32.SetBkMode(hdc, 1)

    windll.gdi32.TextOutW(hdc, text_x, text_y, text, len(text))
    windll.gdi32.SelectObject(hdc, old_hf)
    windll.gdi32.DeleteObject(hf)

try:
    while True:
        for _ in range(10):
            draw_zoom_effect(hdc)
            sleep(0.05)  # Add a delay to make the effect visible

        # Use static text with flashing effect
        static_text = "Furight.exe"
        draw_text(hdc, static_text)

        sleep(0.1)  # Delay between text updates
finally:
    windll.user32.ReleaseDC(0, hdc)
