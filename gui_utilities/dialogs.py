from .structure import label, button
from .system import get_responsive_width
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QApplication
import sys

def information_message_box(
    window_reference,
    text,
    left_margin = 25,
    top_margin = 25,
    right_margin = 25,
    bottom_margin = 25,
    spacing = 10,
    background_color = "#1e1e1e",
    border_width = 2,
    border_color = "#5c5c5c",
    border_radius = 0,
    label_font_family = "Segoe UI",
    label_font_size = 14,
    label_font_color = "#ffffff",
    label_padding = 15,
    label_left_padding = None,
    label_top_padding = None,
    label_right_padding = None,
    label_bottom_padding = None,
    label_border_width = 0,
    label_border_color = "#ffffff",
    label_border_radius = 0,
    button_text = "Aceptar",
    button_font_family = "Segoe UI",
    button_font_size = 14,
    button_font_color = "#ffffff",
    button_background_color = "#1e1e1e",
    button_padding = 15,
    button_left_padding = None,
    button_top_padding = None,
    button_right_padding = None,
    button_bottom_padding = None,
    button_border_width = 2,
    button_border_color = "#5c5c5c",
    button_border_radius = 0,
    button_hover_background_color = "#333333",
    button_hover_border_width = 3,
    button_hover_border_color = "#777777",
    button_pressed_background_color = "#4a4a4a",
    button_pressed_border_width = 3,
    button_pressed_border_color = "#0078d7",
    button_disabled_font_color = "#888888",
    button_disabled_background_color = "#2d2d2d",
    button_disabled_border_width = 2,
    button_disabled_border_color = "#4a4a4a",
    fixed_width = None,
    math_expression = False,
    parent = None
):
    if window_reference is None: window_reference = QApplication.activeWindow()
    message_box = QDialog(parent if parent else window_reference)
    message_box.setObjectName("message_box")
    message_box.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    if fixed_width is None: fixed_width = get_responsive_width(window_reference, 4)
    if fixed_width is not None: message_box.setFixedWidth(fixed_width)
    style_sheet = f"""
        QDialog#message_box {{
            background-color: {background_color};
            border: {border_width}px solid {border_color};
            border-radius: {border_radius}px;
        }}
    """
    message_box.setStyleSheet(style_sheet)
    main_layout = QVBoxLayout(message_box)
    message_box.setLayout(main_layout)
    main_layout.setContentsMargins(left_margin, top_margin, right_margin, bottom_margin)
    main_layout.setSpacing(spacing)
    txt_label = label(
        text = text,
        font_family = label_font_family,
        font_size = label_font_size,
        font_color = label_font_color,
        background_color = "transparent",
        padding = label_padding,
        left_padding = label_left_padding,
        top_padding = label_top_padding,
        right_padding = label_right_padding,
        bottom_padding = label_bottom_padding,
        border_width = label_border_width,
        border_color = label_border_color,
        border_radius = label_border_radius,
        alignment = "center",
        word_wrap = True,
        math_expression = math_expression,
        parent = message_box
    )
    main_layout.addWidget(txt_label)
    button_grid = QGridLayout()
    main_layout.addLayout(button_grid)
    accept_button = button(
        text = button_text,
        font_family = button_font_family,
        font_size = button_font_size,
        font_color = button_font_color,
        background_color = button_background_color,
        padding = button_padding,
        left_padding = button_left_padding,
        top_padding = button_top_padding,
        right_padding = button_right_padding,
        bottom_padding = button_bottom_padding,
        border_width = button_border_width,
        border_color = button_border_color,
        border_radius = button_border_radius,
        hover_background_color = button_hover_background_color,
        hover_border_width = button_hover_border_width,
        hover_border_color = button_hover_border_color,
        pressed_background_color = button_pressed_background_color,
        pressed_border_width = button_pressed_border_width,
        pressed_border_color = button_pressed_border_color,
        disabled_font_color = button_disabled_font_color,
        disabled_background_color = button_disabled_background_color,
        disabled_border_width = button_disabled_border_width,
        disabled_border_color = button_disabled_border_color
    )
    button_grid.addWidget(accept_button)
    accept_button.clicked.connect(message_box.accept)
    return message_box

def confirmation_message_box(
    window_reference,
    text,
    left_margin = 25,
    top_margin = 25,
    right_margin = 25,
    bottom_margin = 25,
    spacing = 10,
    button_spacing = 10,
    background_color = "#1e1e1e",
    border_width = 2,
    border_color = "#5c5c5c",
    border_radius = 0,
    label_font_family = "Segoe UI",
    label_font_size = 14,
    label_font_color = "#ffffff",
    label_padding = 15,
    label_left_padding = None,
    label_top_padding = None,
    label_right_padding = None,
    label_bottom_padding = None,
    label_border_width = 0,
    label_border_color = "#ffffff",
    label_border_radius = 0,
    accept_button_text = "Sí",
    reject_button_text = "No",
    button_font_family = "Segoe UI",
    button_font_size = 14,
    button_font_color = "#ffffff",
    button_background_color = "#1e1e1e",
    button_padding = 15,
    button_left_padding = None,
    button_top_padding = None,
    button_right_padding = None,
    button_bottom_padding = None,
    button_border_width = 2,
    button_border_color = "#5c5c5c",
    button_border_radius = 0,
    button_hover_background_color = "#333333",
    button_hover_border_width = 3,
    button_hover_border_color = "#777777",
    button_pressed_background_color = "#4a4a4a",
    button_pressed_border_width = 3,
    button_pressed_border_color = "#0078d7",
    button_disabled_font_color = "#888888",
    button_disabled_background_color = "#2d2d2d",
    button_disabled_border_width = 2,
    button_disabled_border_color = "#4a4a4a",
    fixed_width = None,
    math_expression = False,
    parent = None
):
    if window_reference is None: window_reference = QApplication.activeWindow()
    message_box = QDialog(parent if parent else window_reference)
    message_box.setObjectName("message_box")
    message_box.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    if fixed_width is None: fixed_width = get_responsive_width(window_reference, 4)
    if fixed_width is not None: message_box.setFixedWidth(fixed_width)
    style_sheet = f"""
        QDialog#message_box {{
            background-color: {background_color};
            border: {border_width}px solid {border_color};
            border-radius: {border_radius}px;
        }}
    """
    message_box.setStyleSheet(style_sheet)
    main_layout = QVBoxLayout(message_box)
    message_box.setLayout(main_layout)
    main_layout.setContentsMargins(left_margin, top_margin, right_margin, bottom_margin)
    main_layout.setSpacing(spacing)
    txt_label = label(
        text = text,
        font_family = label_font_family,
        font_size = label_font_size,
        font_color = label_font_color,
        background_color = "transparent",
        padding = label_padding,
        left_padding = label_left_padding,
        top_padding = label_top_padding,
        right_padding = label_right_padding,
        bottom_padding = label_bottom_padding,
        border_width = label_border_width,
        border_color = label_border_color,
        border_radius = label_border_radius,
        alignment = "center",
        word_wrap = True,
        math_expression = math_expression,
        parent = message_box
    )
    main_layout.addWidget(txt_label)
    button_grid = QGridLayout()
    main_layout.addLayout(button_grid)
    button_grid.setSpacing(button_spacing)
    accept_btn = button(
        text = accept_button_text,
        font_family = button_font_family,
        font_size = button_font_size,
        font_color = button_font_color,
        background_color = button_background_color,
        padding = button_padding,
        left_padding = button_left_padding,
        top_padding = button_top_padding,
        right_padding = button_right_padding,
        bottom_padding = button_bottom_padding,
        border_width = button_border_width,
        border_color = button_border_color,
        border_radius = button_border_radius,
        hover_background_color = button_hover_background_color,
        hover_border_width = button_hover_border_width,
        hover_border_color = button_hover_border_color,
        pressed_background_color = button_pressed_background_color,
        pressed_border_width = button_pressed_border_width,
        pressed_border_color = button_pressed_border_color,
        disabled_font_color = button_disabled_font_color,
        disabled_background_color = button_disabled_background_color,
        disabled_border_width = button_disabled_border_width,
        disabled_border_color = button_disabled_border_color
    )
    reject_btn = button(
        text = reject_button_text,
        font_family = button_font_family,
        font_size = button_font_size,
        font_color = button_font_color,
        background_color = button_background_color,
        padding = button_padding,
        left_padding = button_left_padding,
        top_padding = button_top_padding,
        right_padding = button_right_padding,
        bottom_padding = button_bottom_padding,
        border_width = button_border_width,
        border_color = button_border_color,
        border_radius = button_border_radius,
        hover_background_color = button_hover_background_color,
        hover_border_width = button_hover_border_width,
        hover_border_color = button_hover_border_color,
        pressed_background_color = button_pressed_background_color,
        pressed_border_width = button_pressed_border_width,
        pressed_border_color = button_pressed_border_color,
        disabled_font_color = button_disabled_font_color,
        disabled_background_color = button_disabled_background_color,
        disabled_border_width = button_disabled_border_width,
        disabled_border_color = button_disabled_border_color
    )
    button_grid.addWidget(accept_btn, 0, 0)
    button_grid.addWidget(reject_btn, 0, 1)
    accept_btn.clicked.connect(message_box.accept)
    reject_btn.clicked.connect(message_box.reject)
    return message_box

def confirm_exit(
    window_reference,
    background_color = "#1e1e1e",
    border_width = 2,
    border_color = "#5c5c5c",
    border_radius = 0,
    label_font_family = "Segoe UI",
    label_font_size = 14,
    label_font_color = "#ffffff",
    label_padding = 15,
    label_left_padding = None,
    label_top_padding = None,
    label_right_padding = None,
    label_bottom_padding = None,
    label_border_width = 0,
    label_border_color = "#ffffff",
    label_border_radius = 0,
    accept_button_text = "Sí",
    reject_button_text = "No",
    button_font_family = "Segoe UI",
    button_font_size = 14,
    button_font_color = "#ffffff",
    button_background_color = "#1e1e1e",
    button_padding = 15,
    button_left_padding = None,
    button_top_padding = None,
    button_right_padding = None,
    button_bottom_padding = None,
    button_border_width = 2,
    button_border_color = "#5c5c5c",
    button_border_radius = 0,
    button_hover_background_color = "#333333",
    button_hover_border_width = 3,
    button_hover_border_color = "#777777",
    button_pressed_background_color = "#4a4a4a",
    button_pressed_border_width = 3,
    button_pressed_border_color = "#0078d7",
    button_disabled_font_color = "#888888",
    button_disabled_background_color = "#2d2d2d",
    button_disabled_border_width = 2,
    button_disabled_border_color = "#4a4a4a"
):
    message_box = confirmation_message_box(
        window_reference = window_reference,
        text = "¿Está seguro de que desea salir?",
        background_color = background_color,
        border_width = border_width,
        border_color = border_color,
        border_radius = border_radius,
        label_font_family = label_font_family,
        label_font_size = label_font_size,
        label_font_color = label_font_color,
        label_padding = label_padding,
        label_left_padding = label_left_padding,
        label_top_padding = label_top_padding,
        label_right_padding = label_right_padding,
        label_bottom_padding = label_bottom_padding,
        label_border_width = label_border_width,
        label_border_color = label_border_color,
        label_border_radius = label_border_radius,
        accept_button_text = accept_button_text,
        reject_button_text = reject_button_text,
        button_font_family = button_font_family,
        button_font_size = button_font_size,
        button_font_color = button_font_color,
        button_background_color = button_background_color,
        button_padding = button_padding,
        button_left_padding = button_left_padding,
        button_top_padding = button_top_padding,
        button_right_padding = button_right_padding,
        button_bottom_padding = button_bottom_padding,
        button_border_width = button_border_width,
        button_border_color = button_border_color,
        button_border_radius = button_border_radius,
        button_hover_background_color = button_hover_background_color,
        button_hover_border_width = button_hover_border_width,
        button_hover_border_color = button_hover_border_color,
        button_pressed_background_color = button_pressed_background_color,
        button_pressed_border_width = button_pressed_border_width,
        button_pressed_border_color = button_pressed_border_color,
        button_disabled_font_color = button_disabled_font_color,
        button_disabled_background_color = button_disabled_background_color,
        button_disabled_border_width = button_disabled_border_width,
        button_disabled_border_color = button_disabled_border_color,
        parent = window_reference
    )
    if message_box.exec(): sys.exit()