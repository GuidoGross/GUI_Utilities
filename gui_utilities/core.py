from PyQt6.QtWidgets import QWidget, QApplication

def window(title, background_color = "#333333"):
    main_window = QWidget()
    main_window.setWindowTitle(title)
    main_window.setStyleSheet(f"background-color: {background_color};")
    main_window.showMaximized()
    return main_window

def switch_instance(window_reference, next_instance_class, *args, **kwargs):
    if window_reference is None: window_reference = QApplication.activeWindow()
    if window_reference:
        window_reference.close()
        window_reference.next_instance = next_instance_class(*args, **kwargs)
        window_reference.next_instance.show()

def clear_layout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None: widget.deleteLater()
            else: clear_layout(item.layout())

def switch_content_widget(window_reference, content_widget):
    if window_reference is None: window_reference = QApplication.activeWindow()
    if hasattr(window_reference, "content_widget"):
        clear_layout(window_reference.content_widget.layout())
        window_reference.content_widget.layout().addWidget(content_widget)