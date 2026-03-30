from .system import _get_alignment_flag, get_resources_path
from .format import html_expression_format
from PyQt6.QtCore import Qt, QSize, QObject, QEvent
from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QComboBox, QToolButton, QWidgetAction, QCheckBox, QScrollArea, QWidget, QSizePolicy,
    QApplication, QStyle, QStyledItemDelegate, QTableWidget, QHeaderView)
from PyQt6.QtGui import QIcon, QTextDocument

def menu(
    window_reference,
    buttons,
    title_text,
    title_font_family = "Segoe UI",
    title_font_size = 36,
    title_font_color = "#ffffff",
    title_background_color = "#1e1e1e",
    title_padding = 15,
    title_left_padding = None,
    title_top_padding = None,
    title_right_padding = None,
    title_bottom_padding = None,
    title_border_width = 0,
    title_border_color = "#ffffff",
    title_border_radius = 0,
    scrollbar_background_color = "#1e1e1e",
    scrollbar_handle_background_color = "#4a4a4a",
    hover_scrollbar_handle_background_color = "#333333",
    hover_scrollbar_handle_border_width = 3,
    hover_scrollbar_handle_border_color = "#777777",
    pressed_scrollbar_handle_background_color = "#333333",
    pressed_scrollbar_handle_border_width = 3,
    pressed_scrollbar_handle_border_color = "#0078d7",
    title_alignment = "center",
    math_expression = False
):
    title_alignment = _get_alignment_flag(title_alignment)
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(25, 25, 25, 25)
    main_layout.addLayout(title(
        text = title_text,
        font_family = title_font_family,
        font_size = title_font_size,
        font_color = title_font_color,
        background_color = title_background_color,
        padding = title_padding,
        left_padding = title_left_padding,
        top_padding = title_top_padding,
        right_padding = title_right_padding,
        bottom_padding = title_bottom_padding,
        border_width = title_border_width,
        border_color = title_border_color,
        border_radius = title_border_radius,
        alignment = title_alignment,
        math_expression = math_expression
    ))
    body_layout = QHBoxLayout()
    main_layout.addLayout(body_layout)
    body_layout.setSpacing(25)
    menu_layout = QVBoxLayout()
    body_layout.addLayout(menu_layout)
    menu_layout.setSpacing(10)
    normal_buttons = []
    special_buttons = []
    for button_properties in buttons:
        if button_properties.get("text") in ["Atrás", "Salir"]: special_buttons.append(button_properties)
        else: normal_buttons.append(button_properties)
    for button_properties in normal_buttons:
        button_properties_copy = button_properties.copy()
        callback = button_properties_copy.pop("callback", None)
        btn = button(**button_properties_copy)
        if callback: btn.clicked.connect(callback)
        menu_layout.addWidget(btn)
    menu_layout.addStretch()
    for button_properties in special_buttons:
        button_properties_copy = button_properties.copy()
        callback = button_properties_copy.pop("callback", None)
        button_properties_copy.setdefault("font_size", 16)
        btn = button(**button_properties_copy)
        if callback: btn.clicked.connect(callback)
        menu_layout.addWidget(btn)
    if window_reference is None: window_reference = QApplication.activeWindow()
    window_reference.content_widget = QWidget()
    window_reference.content_widget.setLayout(QVBoxLayout())
    window_reference.content_widget.setStyleSheet("background-color: #333333;")
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(window_reference.content_widget)
    style_sheet = f"""
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        QScrollBar:vertical {{
            background-color: {scrollbar_background_color};
            border: none;
        }}
        QScrollBar::handle:vertical {{
            background-color: {scrollbar_handle_background_color};
            border: none;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {hover_scrollbar_handle_background_color};
            border: {hover_scrollbar_handle_border_width}px solid {hover_scrollbar_handle_border_color};
        }}
        QScrollBar::handle:vertical:pressed {{
            background-color: {pressed_scrollbar_handle_background_color};
            border: {pressed_scrollbar_handle_border_width}px solid {pressed_scrollbar_handle_border_color};
        }}
    """
    scroll_area.setStyleSheet(style_sheet)
    body_layout.addWidget(scroll_area)
    body_layout.setStretch(0, 1)
    body_layout.setStretch(1, 4)
    return main_layout

def header(
    title_text,
    left_margin = 25,
    top_margin = 25,
    right_margin = 25,
    bottom_margin = 25,
    title_font_family = "Segoe UI",
    title_font_size = 36,
    title_font_color = "#ffffff",
    title_background_color = "#1e1e1e",
    title_padding = 15,
    title_left_padding = None,
    title_top_padding = None,
    title_right_padding = None,
    title_bottom_padding = None,
    title_border_width = 0,
    title_border_color = "#ffffff",
    title_border_radius = 0,
    title_alignment = "center",
    math_expression = False
):
    title_alignment = _get_alignment_flag(title_alignment)
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(left_margin, top_margin, right_margin, bottom_margin)
    title_layout = title(
        text = title_text,
        font_family = title_font_family,
        font_size = title_font_size,
        font_color = title_font_color,
        background_color = title_background_color,
        padding = title_padding,
        left_padding = title_left_padding,
        top_padding = title_top_padding,
        right_padding = title_right_padding,
        bottom_padding = title_bottom_padding,
        border_width = title_border_width,
        border_color = title_border_color,
        border_radius = title_border_radius,
        alignment = title_alignment,
        math_expression = math_expression
    )
    main_layout.addLayout(title_layout)
    main_layout.addStretch()
    return main_layout

def title(
    text,
    font_family = "Segoe UI",
    font_size = 36,
    font_color = "#ffffff",
    background_color = "transparent",
    padding = 15,
    left_padding = None,
    top_padding = None,
    right_padding = None,
    bottom_padding = None,
    border_width = 0,
    border_color = "#ffffff",
    border_radius = 0,
    alignment = "center",
    math_expression = False
):
    alignment = _get_alignment_flag(alignment)
    title_layout = QHBoxLayout()
    title_layout.setContentsMargins(0, 0, 0, 25)
    title_label = label(
        text = text,
        font_family = font_family,
        font_size = font_size,
        font_color = font_color,
        font_weight = "bold",
        background_color = background_color,
        padding = padding,
        left_padding = left_padding,
        top_padding = top_padding,
        right_padding = right_padding,
        bottom_padding = bottom_padding,
        border_width = border_width,
        border_color = border_color,
        border_radius = border_radius,
        alignment = alignment,
        math_expression = math_expression
    )
    title_layout.addWidget(title_label)
    return title_layout

def label(
        text,
        font_family = "Segoe UI",
        font_size = 14,
        font_color = "#ffffff",
        font_weight = "normal",
        background_color = "transparent",
        padding = 15,
        left_padding = None,
        top_padding = None,
        right_padding = None,
        bottom_padding = None,
        border_width = 0,
        border_color = "#5c5c5c",
        border_radius = 0,
        hover_background_color = "transparent",
        hover_border_width = 0,
        hover_border_color = "#777777",
        disabled_font_color = "#888888",
        disabled_background_color = "transparent",
        disabled_border_width = 0,
        disabled_border_color = "#4a4a4a",
        alignment = "left",
        maximum_width = None,
        word_wrap = False,
        math_expression = False,
        transparent_for_mouse = False,
        parent = None
):
    if math_expression:
        lbl = QLabel(html_expression_format(text), parent)
        lbl.setTextFormat(Qt.TextFormat.RichText)
    else: lbl = QLabel(text, parent)
    alignment = _get_alignment_flag(alignment)
    if maximum_width is not None: lbl.setMaximumWidth(maximum_width)
    if transparent_for_mouse: lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
    if alignment: lbl.setAlignment(alignment)
    if word_wrap: lbl.setWordWrap(True)
    left_padding_value = left_padding if left_padding is not None else padding
    top_padding_value = top_padding if top_padding is not None else padding
    right_padding_value = right_padding if right_padding is not None else padding
    bottom_padding_value = bottom_padding if bottom_padding is not None else padding
    style_sheet = f"""
        QLabel {{
            font-family: {font_family};
            font-size: {font_size}px;
            color: {font_color};
            font-weight: {font_weight};
            background-color: {background_color};
            padding-left: {left_padding_value}px;
            padding-top: {top_padding_value}px;
            padding-right: {right_padding_value}px;
            padding-bottom: {bottom_padding_value}px;
            border: {border_width}px solid {border_color};
            border-radius: {border_radius}px;
        }}
        QLabel:hover{{
            background-color: {hover_background_color};
            border: {hover_border_width}px solid {hover_border_color};
        }}
        QLabel:disabled{{
            color: {disabled_font_color};
            background-color: {disabled_background_color};
            border: {disabled_border_width}px solid {disabled_border_color};
        }}
    """
    lbl.setStyleSheet(style_sheet)
    return lbl

def button(
    text,
    font_family = "Segoe UI",
    font_size = 14,
    font_color = "#ffffff",
    font_weight = "bold",
    background_color = "#1e1e1e",
    padding = 15,
    left_padding = None,
    top_padding = None,
    right_padding = None,
    bottom_padding = None,
    border_width = 2,
    border_color = "#5c5c5c",
    border_radius = 0,
    hover_background_color = "#333333",
    hover_border_width = 3,
    hover_border_color = "#777777",
    pressed_background_color = "#4a4a4a",
    pressed_border_width = 3,
    pressed_border_color = "#0078d7",
    disabled_font_color = "#888888",
    disabled_background_color = "#2d2d2d",
    disabled_border_width = 2,
    disabled_border_color = "#4a4a4a",
    maximum_width = None,
    alignment = "center",
    math_expression = False,
    parent = None
):
    btn = QPushButton(parent)
    btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
    if maximum_width is not None: btn.setMaximumWidth(maximum_width)
    main_layout = QVBoxLayout()
    btn.setLayout(main_layout)
    main_layout.setContentsMargins(0, 0, 0, 0)
    lbl = label(
        text = text,
        font_size = font_size,
        font_color = font_color,
        font_weight = "bold",
        padding = padding,
        left_padding = left_padding,
        top_padding = top_padding,
        right_padding = right_padding,
        bottom_padding = bottom_padding,
        disabled_border_width = disabled_border_width,
        alignment = alignment,
        word_wrap = True,
        transparent_for_mouse = True,
        math_expression = math_expression
    )
    main_layout.addWidget(lbl)
    left_padding_value = left_padding if left_padding is not None else padding
    top_padding_value = top_padding if top_padding is not None else padding
    right_padding_value = right_padding if right_padding is not None else padding
    bottom_padding_value = bottom_padding if bottom_padding is not None else padding
    style_sheet = f"""
        QPushButton {{
            font-family: {font_family};
            font-size: {font_size}px;
            color: {font_color};
            font-weight: {font_weight};
            background-color: {background_color};
            padding-left: {left_padding_value}px;
            padding-top: {top_padding_value}px;
            padding-right: {right_padding_value}px;
            padding-bottom: {bottom_padding_value}px;
            border: {border_width}px solid {border_color};
            border-radius: {border_radius}px;
        }}
        QPushButton:hover {{
            background-color: {hover_background_color};
            border: {hover_border_width}px solid {hover_border_color};
        }}
        QPushButton:pressed {{
            background-color: {pressed_background_color};
            border: {pressed_border_width}px solid {pressed_border_color};
        }}
        QPushButton:disabled {{
            color: {disabled_font_color};
            background-color: {disabled_background_color};
            border: {disabled_border_width}px solid {disabled_border_color};
        }}
    """
    btn.setStyleSheet(style_sheet)
    return btn

def text_box(
    placeholder_text,
    font_family = "Segoe UI",
    font_size = 14,
    font_color = "#ffffff",
    font_weight = "normal",
    background_color = "#1e1e1e",
    padding = 15,
    left_padding = None,
    top_padding = None,
    right_padding = None,
    bottom_padding = None,
    border_width = 2,
    border_color = "#5c5c5c",
    border_radius = 0,
    placeholder_font_color = "#888888",
    hover_background_color = "#333333",
    hover_border_width = 3,
    hover_border_color = "#777777",
    focus_font_color = "#000000",
    focus_background_color = "#ffffff",
    focus_border_width = 3,
    focus_border_color = "#0078d7",
    disabled_font_color = "#888888",
    disabled_background_color = "#2d2d2d",
    disabled_border_width = 2,
    disabled_border_color = "#4a4a4a",
    show_text_icon_url = None,
    hide_text_icon_url = None,
    focused_show_text_icon_url = None,
    focused_hide_text_icon_url = None,
    hide_text = False,
    math_expression = False,
    parent = None
):
    if show_text_icon_url is None: show_text_icon_url = get_resources_path("icons/show_text_icon.png")
    if hide_text_icon_url is None: hide_text_icon_url = get_resources_path("icons/hide_text_icon.png")
    if focused_show_text_icon_url is None: focused_show_text_icon_url = get_resources_path("icons/focused_show_text_icon.png")
    if focused_hide_text_icon_url is None: focused_hide_text_icon_url = get_resources_path("icons/focused_hide_text_icon.png")
    txt_box = QLineEdit(parent)
    left_padding_value = left_padding if left_padding is not None else padding
    top_padding_value = top_padding if top_padding is not None else padding
    right_padding_value = right_padding if right_padding is not None else padding
    bottom_padding_value = bottom_padding if bottom_padding is not None else padding
    style_sheet = f"""
        QLineEdit {{
            font-family: {font_family};
            font-size: {font_size}px;
            color: {font_color};
            font-weight: {font_weight};
            background-color: {background_color};
            padding-left: {left_padding_value}px;
            padding-top: {top_padding_value}px;
            padding-right: {right_padding_value}px;
            padding-bottom: {bottom_padding_value}px;
            border: {border_width}px solid {border_color};
            border-radius: {border_radius}px;
        }}
        QLineEdit:hover {{
            background-color: {hover_background_color};
            border: {hover_border_width}px solid {hover_border_color};
        }}
        QLineEdit:focus {{
            color: {focus_font_color};
            background-color: {focus_background_color};
            border: {focus_border_width}px solid {focus_border_color};
        }}
        QLineEdit:disabled {{
            color: {disabled_font_color};
            background-color: {disabled_background_color};
            border: {disabled_border_width}px solid {disabled_border_color};
        }}
    """
    txt_box.setStyleSheet(style_sheet)
    toggle_text_visibility_button = None
    if hide_text:
        show_text_icon = QIcon(show_text_icon_url)
        hide_text_icon = QIcon(hide_text_icon_url)
        focused_show_text_icon = QIcon(focused_show_text_icon_url)
        focused_hide_text_icon = QIcon(focused_hide_text_icon_url)
        txt_box.setEchoMode(QLineEdit.EchoMode.Password)
        toggle_text_visibility_button = QToolButton(txt_box)
        toggle_text_visibility_button.setCursor(Qt.CursorShape.PointingHandCursor)
        toggle_text_visibility_button.setAutoRaise(True)
        toggle_text_visibility_button.setIcon(show_text_icon)
        toggle_text_visibility_button.setIconSize(QSize(25, 25))
        toggle_text_visibility_action = QWidgetAction(txt_box)
        toggle_text_visibility_action.setDefaultWidget(toggle_text_visibility_button)
        txt_box.addAction(toggle_text_visibility_action, QLineEdit.ActionPosition.TrailingPosition)
        toggle_text_visibility_button.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                border: none;
                margin-right: 10px;
            }
        """)
        
        def update_icon():
            is_password = txt_box.echoMode() == QLineEdit.EchoMode.Password
            if txt_box.hasFocus():
                icon = focused_show_text_icon if is_password else focused_hide_text_icon
            else: icon = show_text_icon if is_password else hide_text_icon
            toggle_text_visibility_button.setIcon(icon)
        
        def toggle_visibility():
            if txt_box.echoMode() == QLineEdit.EchoMode.Password:
                txt_box.setEchoMode(QLineEdit.EchoMode.Normal)
            else: txt_box.setEchoMode(QLineEdit.EchoMode.Password)
            update_icon()
        
        toggle_text_visibility_button.clicked.connect(toggle_visibility)

        class _IconFocusWatcher(QObject):
            def __init__(self, watched, on_focus_change):
                super().__init__(watched)
                self._watched = watched
                self._on_focus_change = on_focus_change
            
            def eventFilter(self, watched, event):
                if watched is self._watched and event.type() in (QEvent.Type.FocusIn, QEvent.Type.FocusOut):
                    if callable(self._on_focus_change): self._on_focus_change()
                return super().eventFilter(watched, event)
        
        icon_focus_watcher = _IconFocusWatcher(txt_box, update_icon)
        txt_box.installEventFilter(icon_focus_watcher)
        setattr(txt_box, "_icon_focus_watcher", icon_focus_watcher)
    placeholder_label = label(
        text = placeholder_text,
        font_family = font_family,
        font_size = font_size,
        font_color = placeholder_font_color,
        font_weight = font_weight,
        padding = padding,
        left_padding = left_padding,
        top_padding = top_padding,
        right_padding = right_padding,
        bottom_padding = bottom_padding,
        math_expression = math_expression,
        transparent_for_mouse = True,
        parent = txt_box
    )
    placeholder_label.move(0, 2)
    
    def update_placeholder_visibility():
        has_text = bool(txt_box.text().strip())
        has_focus = txt_box.hasFocus()
        placeholder_label.setVisible(not has_text and not has_focus)
        if hide_text and toggle_text_visibility_button: update_icon()
    
    txt_box.textChanged.connect(update_placeholder_visibility)
    
    class _PlaceholderFocusWatcher(QObject):
        def __init__(self, watched, on_focus_change):
            super().__init__(watched)
            self._watched = watched
            self._on_focus_change = on_focus_change
        
        def eventFilter(self, watched, event):
            if watched is self._watched and event.type() in (QEvent.Type.FocusIn, QEvent.Type.FocusOut):
                if callable(self._on_focus_change): self._on_focus_change()
            return super().eventFilter(watched, event)
    
    placeholder_focus_watcher = _PlaceholderFocusWatcher(txt_box, update_placeholder_visibility)
    txt_box.installEventFilter(placeholder_focus_watcher)
    setattr(txt_box, "_placeholder_focus_watcher", placeholder_focus_watcher)
    update_placeholder_visibility()
    return txt_box

def combo_box(
    placeholder_text,
    items,
    font_family = "Segoe UI",
    font_size = 14,
    placeholder_font_color = "#888888",
    font_color = "#ffffff",
    background_color = "#1e1e1e",
    padding = 15,
    left_padding = None,
    top_padding = None,
    right_padding = None,
    bottom_padding = None,
    border_width = 2,
    border_color = "#5c5c5c",
    border_radius = 0,
    hover_background_color = "#333333",
    hover_border_width = 3,
    hover_border_color = "#777777",
    disabled_font_color = "#888888",
    disabled_background_color = "#2d2d2d",
    disabled_border_width = 2,
    disabled_border_color = "#4a4a4a",
    on_font_color = "#000000",
    on_background_color = "#ffffff",
    on_border_width = 3,
    on_border_color = "#0078d7",
    dropdown_font_color = "#ffffff",
    dropdown_background_color = "#1e1e1e",
    dropdown_selection_background_color = "#0078d7",
    dropdown_border_width = 1,
    dropdown_border_color = "#5c5c5c",
    math_expression = False,
    parent = None
):
    cmb_box = QComboBox(parent)
    cmb_box.setAccessibleName("combo_box")
    left_padding_value = left_padding if left_padding is not None else padding
    top_padding_value = top_padding if top_padding is not None else padding
    right_padding_value = right_padding if right_padding is not None else padding
    bottom_padding_value = bottom_padding if bottom_padding is not None else padding
    placeholder_label = None
    if math_expression:
        placeholder_label = label(
            text = placeholder_text,
            font_family = font_family,
            font_size = font_size,
            font_color = placeholder_font_color,
            padding = padding,
            left_padding = left_padding,
            top_padding = top_padding,
            right_padding = right_padding,
            bottom_padding = bottom_padding,
            math_expression = True,
            transparent_for_mouse = True,
            parent = cmb_box
        )
        placeholder_label.move(0, 2)

        def update_placeholder_visibility():
            has_selection = cmb_box.currentIndex() != -1
            placeholder_label.setVisible(not has_selection)
        
        cmb_box.currentIndexChanged.connect(update_placeholder_visibility)
        update_placeholder_visibility()

        class RichTextDelegate(QStyledItemDelegate):
            def __init__(
                self,
                parent = None,
                font_color = "#ffffff",
                selection_font_color = "#ffffff"
            ):
                super().__init__(parent)
                self.font_color = font_color
                self.selection_font_color = selection_font_color
            
            def paint(self, painter, option, index):
                if option.state & QStyle.StateFlag.State_Selected: text_color = self.selection_font_color
                else: text_color = self.font_color
                document = QTextDocument()
                html = f"<span style = \"color:{text_color};\">{index.data(Qt.ItemDataRole.DisplayRole)}</span>"
                document.setHtml(html)
                option.text = ""
                QApplication.style().drawControl(QStyle.ControlElement.CE_ItemViewItem, option, painter)
                painter.save()
                painter.translate(
                    option.rect.left(), option.rect.top() + (option.rect.height() - document.size().height()) / 2
                )
                document.drawContents(painter)
                painter.restore()
        delegate = RichTextDelegate(
            parent = cmb_box,
            font_color = dropdown_font_color,
            selection_font_color = font_color
        )
        cmb_box.setItemDelegate(delegate)
        cmb_box.clear()
        for item in items: cmb_box.addItem(html_expression_format(item))
        cmb_box.view().setTextElideMode(Qt.TextElideMode.ElideNone)
    else:
        cmb_box.setPlaceholderText(placeholder_text)
        cmb_box.addItems(items)
    cmb_box.setCurrentIndex(-1)
    selected_item_label = None
    if math_expression:
        selected_item_label = label(
            text = "",
            font_family = font_family,
            font_size = font_size,
            font_color = font_color,
            padding = padding,
            left_padding = left_padding,
            top_padding = top_padding,
            right_padding = right_padding,
            bottom_padding = bottom_padding,
            math_expression = True,
            transparent_for_mouse = True,
            parent = cmb_box
        )
        selected_item_label.setVisible(False)

        def update_selected_item_display(index):
            if index != -1:
                html_text = cmb_box.itemText(index)
                selected_item_label.setText(html_text)
                selected_item_label.setVisible(True)
            else: selected_item_label.setVisible(False)
        
        cmb_box.currentIndexChanged.connect(update_selected_item_display)
    
    def get_stylesheet(font_color):
        return f"""
            QComboBox[accessibleName="combo_box"] {{
                font-family: {font_family};
                font-size: {font_size}px;
                color: {font_color};
                background-color: {background_color};
                padding-left: {left_padding_value}px;
                padding-top: {top_padding_value}px;
                padding-right: {right_padding_value}px;
                padding-bottom: {bottom_padding_value}px;
                border: {border_width}px solid {border_color};
                border-radius: {border_radius}px;
            }}
            QComboBox[accessibleName="combo_box"]:hover {{
                background-color: {hover_background_color};
                border: {hover_border_width}px solid {hover_border_color};
            }}
            QComboBox[accessibleName="combo_box"]:disabled {{
                color: {disabled_font_color};
                background-color: {disabled_background_color};
                border: {disabled_border_width}px solid {disabled_border_color};
            }}
            QComboBox[accessibleName="combo_box"]:on {{
                color: {"transparent" if math_expression else on_font_color};
                background-color: {on_background_color};
                border: {on_border_width}px solid {on_border_color};
            }}
            QComboBox QAbstractItemView {{
                color: {dropdown_font_color};
                background-color: {dropdown_background_color};
                selection-background-color: {dropdown_selection_background_color};
                border: {dropdown_border_width}px solid {dropdown_border_color};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
        """
    
    def change_color(index):
        if index == -1:
            text_color = "transparent" if math_expression else placeholder_font_color
            cmb_box.setStyleSheet(get_stylesheet(text_color))
        else:
            text_color = "transparent" if math_expression else font_color
            cmb_box.setStyleSheet(get_stylesheet(text_color))
    
    cmb_box.currentIndexChanged.connect(change_color)
    change_color(-1)
    return cmb_box

def check_box(
    text,
    font_family = "Segoe UI",
    font_size = 14,
    font_color = "#ffffff",
    background_color = "#1e1e1e",
    padding = 5,
    left_padding = None,
    top_padding = None,
    right_padding = None,
    bottom_padding = None,
    indicator_background_color = "#1e1e1e",
    indicator_border_width = 1,
    indicator_border_color = "#5c5c5c",
    indicator_border_radius = 8,
    hover_indicator_background_color = "#333333",
    hover_indicator_border_width = 2,
    hover_indicator_border_color = "#777777",
    pressed_indicator_background_color = "#4a4a4a",
    pressed_indicator_border_width = 2,
    pressed_indicator_border_color = "#0078d7",
    checked_indicator_background_color = "#ffffff",
    checked_indicator_border_width = 1,
    checked_indicator_border_color = "#5c5c5c",
    disabled_font_color = "#888888",
    disabled_background_color = "#2d2d2d",
    disabled_border_width = 1,
    disabled_border_color = "#4a4a4a",
    parent = None
):
    chk_box = QCheckBox(text, parent)
    left_padding_value = left_padding if left_padding is not None else padding
    top_padding_value = top_padding if top_padding is not None else padding
    right_padding_value = right_padding if right_padding is not None else padding
    bottom_padding_value = bottom_padding if bottom_padding is not None else padding
    style_sheet = f"""
        QCheckBox {{
            font-family: {font_family};
            font-size: {font_size}px;
            color: {font_color};
            background-color: {background_color};
            padding-left: {left_padding_value}px;
            padding-top: {top_padding_value}px;
            padding-right: {right_padding_value}px;
            padding-bottom: {bottom_padding_value}px;
        }}
        QCheckBox::indicator {{
            image: none;
            width: {font_size}px;
            height: {font_size}px;
            background-color: {indicator_background_color};
            border: {indicator_border_width}px solid {indicator_border_color};
            border-radius: {indicator_border_radius}px;
        }}
        QCheckBox::indicator:hover {{
            background-color: {hover_indicator_background_color};
            border: {hover_indicator_border_width}px solid {hover_indicator_border_color};
        }}
        QCheckBox::indicator:pressed {{
            background-color: {pressed_indicator_background_color};
            border: {pressed_indicator_border_width}px solid {pressed_indicator_border_color};
        }}
        QCheckBox::indicator:checked {{
            background-color: {checked_indicator_background_color};
            border: {checked_indicator_border_width}px solid {checked_indicator_border_color};
        }}
        QCheckBox:disabled {{
            color: {disabled_font_color};
        }}
        QCheckBox::indicator:disabled {{
            background-color: {disabled_background_color};
            border: {disabled_border_width}px solid {disabled_border_color};
        }}
    """ 
    chk_box.setStyleSheet(style_sheet)
    return chk_box

def table(
    items_data,
    column_headers,
    column_proportions,
    row_populator_function,
    font_family = "Segoe UI",
    font_size = 14,
    font_color = "#ffffff",
    background_color = "#1e1e1e",
    border_width = 2,
    border_color = "#5c5c5c",
    item_font_color = "#ffffff",
    item_background_color = "#1e1e1e",
    selected_item_background_color = "#0078d7",
    item_alignment = "center",
    header_font_family = "Segoe UI",
    header_font_size = 14,
    header_font_color = "#ffffff",
    header_font_weight = "bold",
    header_background_color = "#1e1e1e",
    header_border_width = 1,
    header_border_color = "#191919",
    hover_header_background_color = "#333333",
    hover_header_border_width = 3,
    hover_header_border_color = "#777777",
    pressed_header_background_color = "#4a4a4a",
    pressed_header_border_width = 3,
    pressed_header_border_color = "#0078d7",
    scrollbar_background_color = "#1e1e1e",
    scrollbar_handle_background_color = "#333333",
    hover_scrollbar_handle_background_color = "#4a4a4a",
    hover_scrollbar_handle_border_width = 3,
    hover_scrollbar_handle_border_color = "#777777",
    pressed_scrollbar_handle_background_color = "#4a4a4a",
    pressed_scrollbar_handle_border_width = 3,
    pressed_scrollbar_handle_border_color = "#0078d7",
    parent = None
):
    table_widget = QTableWidget(parent)
    table_widget.verticalHeader().setVisible(False)
    table_widget.setColumnCount(len(column_headers))
    table_widget.setHorizontalHeaderLabels(column_headers)
    hdr = table_widget.horizontalHeader()
    hdr.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
    
    def resize_columns():
        total_width = table_widget.viewport().width()
        if total_width == 0: return
        for i, proportion in enumerate(column_proportions):
            table_widget.setColumnWidth(i, int(total_width * proportion))
    
    resize_columns()
    original_resize_event = table_widget.resizeEvent

    def on_resize(event):
        resize_columns()
        if original_resize_event: original_resize_event(event)
    
    table_widget.resizeEvent = on_resize
    style_sheet = f"""
        QTableWidget {{
            color: {font_color};
            background-color: {background_color};
            font-family: {font_family};
            font-size: {font_size}px;
            border: {border_width}px solid {border_color};
        }}
        QTableWidget::item {{
            color: {item_font_color};
            background-color: {item_background_color};
            border: none;
        }}
        QTableWidget::item:selected {{
            background-color: {selected_item_background_color};
        }}
        QHeaderView::section {{
            color: {header_font_color};
            background-color: {header_background_color};
            font-family: {header_font_family};
            font-size: {header_font_size}px;
            font-weight: {header_font_weight};
            border: {header_border_width}px solid {header_border_color};
        }}
        QHeaderView::section:hover {{
            background-color: {hover_header_background_color};
            border: {hover_header_border_width}px solid {hover_header_border_color};
        }}
        QHeaderView::section:pressed {{
            background-color: {pressed_header_background_color};
            border: {pressed_header_border_width}px solid {pressed_header_border_color};
        }}
        QScrollBar:vertical {{
            background-color: {scrollbar_background_color};
            border: none;
        }}
        QScrollBar::handle:vertical {{
            background-color: {scrollbar_handle_background_color};
            border: none;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {hover_scrollbar_handle_background_color};
            border: {hover_scrollbar_handle_border_width}px solid {hover_scrollbar_handle_border_color};
        }}
        QScrollBar::handle:vertical:pressed {{
            background-color: {pressed_scrollbar_handle_background_color};
            border: {pressed_scrollbar_handle_border_width}px solid {pressed_scrollbar_handle_border_color};
        }}
    """
    table_widget.setStyleSheet(style_sheet)
    table_widget.setRowCount(len(items_data))
    alignment_flag = _get_alignment_flag(item_alignment)
    for row, item_data in enumerate(items_data):
        items = row_populator_function(item_data)
        if alignment_flag:
            for item in items: item.setTextAlignment(alignment_flag)
        for column, item in enumerate(items): table_widget.setItem(row, column, item)
    return table_widget