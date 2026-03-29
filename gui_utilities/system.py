import os
import sys

def in_google_colaboratory(): return "google.colab" in sys.modules or "ipykernel" in sys.modules

if not in_google_colaboratory():
    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import QApplication

def _get_alignment_flag(aligment):
    if not isinstance(aligment, str): return aligment
    alignment_map = {
        "left": Qt.AlignmentFlag.AlignLeft,
        "right": Qt.AlignmentFlag.AlignRight,
        "center": Qt.AlignmentFlag.AlignCenter,
        "justify": Qt.AlignmentFlag.AlignJustify,
        "top": Qt.AlignmentFlag.AlignTop,
        "bottom": Qt.AlignmentFlag.AlignBottom,
        "middle": Qt.AlignmentFlag.AlignVCenter
    }
    parts = aligment.lower().split()
    if not parts: return None
    final_alignment = Qt.AlignmentFlag(0)
    for part in parts: final_alignment |= alignment_map.get(part, Qt.AlignmentFlag(0))
    return final_alignment if final_alignment != Qt.AlignmentFlag(0) else None

def get_responsive_width(window, fraction = 3.0):
    if window: screen = window.screen()
    else: screen = QApplication.primaryScreen()
    if screen: screen_width = screen.size().width()
    else: screen_width = 1920
    return round(screen_width / fraction)

def get_resources_path(relative_path, base_path = None):
    if hasattr(sys, "_MEIPASS"): return os.path.join(sys._MEIPASS, relative_path)
    if base_path is None: base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)