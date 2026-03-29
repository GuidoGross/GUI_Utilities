# **GUI Utilities**

Personal-use graphical utilities library providing styled PyQt6 interaction, structured menus, robust input validation, formatting helpers, and Spanish-oriented user experience.

---

## **Purpose**

**This library is designed for graphical applications that need:**

- Clean UI
- Structured Spanish-language user interaction
- Robust validation
- Consistent formatting

---

## **Requirements**

### **Dependencies**

**Standard library modules are used where possible; only external dependencies are listed:**

- PyQt6 (6.2.0 or higher)
- matplotlib (3.5.0 or higher)
- numpy (1.21.3 or higher)
- pandas (1.3.4 or higher)
- requests (2.25.0 or higher)

### **Python version**

Python (3.10 or higher)

### **Operating System**

**Any of the following:**

- Windows (10, version 1809 or higher)
- Linux (any modern distribution with glibc 2.28 or higher)
- MacOS (10.14 or higher)

### **Google Colaboratory support**

Most of this library is not compatible with Google Colaboratory, since PyQt6 graphical windows cannot run in a headless environment. However, the following modules are fully compatible:

- **Graphs Utilities (graphs):** the entire module.
- **Formatting Helpers (format):** the entire module.
- **Input Validation (validation):** the entire module except "validate_email()".
- **System Utilities (system):** the entire module except "get_responsive_width()".

---

## **Features**

### **Core Utilities (core)**

**Foundational functions for window management and instance control:**

- **window():** creates a base window already configured with layout and initial styles.
- **switch_instance():** dynamically switches the active window instance with a new one.
- **clear_layout():** recursively clears and deletes all widgets within a layout.
- **switch_content_widget():** dynamically switches the content of the main window's internal widget.

### **Structure Utilities (structure)**

**Tools for building UI elements and structures in graphical applications:**

- **menu():** creates interactive selection menus with header, scrolling, and custom buttons.
- **header():** creates a styled header layout, consisting of a title and a separator.
- **title():** creates customized titles for windows or menus.
- **label():** creates customized text labels with rich HTML formatting options.
- **button():** creates customized interactive buttons with hover and pressed styles.
- **text_box():** creates customized text inputs with placeholder text and password visibility toggles.
- **combo_box():** creates customized drop-down lists with rich text formatting.
- **check_box():** creates customized checkboxes with styled indicators.
- **table():** creates personalized tables with easy introduction of fully-styled columns and rows (with responsive resizing).

### **Dialogs Utilities (dialogs)**

**Pop-up and modal dialog management:**

- **information_message_box():** creates customized information dialog boxes.
- **confirmation_message_box():** creates customized confirmation dialog boxes.
- **confirm_exit():** creates a confirmation dialog that exits the program safely (uses confirmation_message_box()).

### **Graphs Utilities (graphs)**

**Helpers for creating customizable statistical and analytical charts:**

- **bar_chart():** creates customizable bar charts for categorical or indexed frequency data.
- **pie_chart():** creates customizable pie charts with color palettes generation.
- **histogram():** creates customizable histograms with optional frequency polygon overlays and interval-based labels.
- **line_chart():** creates customizable line charts with optional filled area display.
- **scatter_plot():** creates customizable scatter plots, including bubble charts through variable marker sizes.
- **heat_map():** creates customizable heat maps with color palettes generation and optional color bars.
- **radar_chart():** creates customizable radar charts for comparing values across multiple categories.

### **Input Validation (validation)**

**Interactive validation utilities using UI dialogs for user input:**

- **check_if_list_is_empty():** checks if a list is empty and displays an error dialog if it is.
- **validate_option():** validates user selection from a list of options.
- **validate_string():** ensures non-empty string input.
- **validate_integer():** validates integers (uses Continental European numeric format) with optional range validation through an advanced syntax (syntax example: "(-infinity; 0] | 5 | [10; infinity)").
- **validate_double():** validates decimal numbers (uses Continental European numeric format) with support for fractions and mathematical constants ("pi", "e", "tau", "phi") and optional range validation through an advanced syntax (syntax example: "(-infinity; 0,1] | 1/3 | [pi; infinity)").
- **validate_date_time():** validates date and time input (uses Continental European date format with 24-hour time) with selectable year, time and second inclusion.
- **validate_id():** validates Argentinian national ID numbers.
- **validate_cellphone_number():** validates cellphone numbers (uses Argentinian format).
- **validate_email():** validates e-mail addresses using an official TLDs list (from IANA's website) or syntax fallback (in case of not having an internet connection or a locally imported list of TLDs).

### **Formatting Helpers (format)**

**Utilities for applying consistent formatting:**

- **decimal_format():** applies Continental European numeric formatting.
- **date_time_format():** formats datetime objects (uses Continental European date format with 24-hour time) with automatic or custom year, time and second inclusion.
- **id_format():** formats Argentinian national ID numbers.
- **cellphone_number_format():** formats cellphone numbers (uses Argentinian format).
- **html_expression_format():** formats plain-text mathematical expressions (like fractions or superscripts) into HTML code for rich text rendering.
- **convert_to_double():** converts string numbers (with Continental European format) into Python floats.
- **define_equality_symbol():** returns the equality (=) or approximation (≅) symbol depending on if the number has rounding precision constraints.

### **System Utilities (system)**

**Helpers for interacting with the operating system graphical environment:**

- **in_google_colaboratory():** checks if the runtime environment is Google Colaboratory.
- **get_responsive_width():** calculates a responsive width based on screen size to maintain an adaptive UI.
- **get_resources_path():** returns the absolute path to a resource file, regardless of whether the program is running as a script in an IDE or as an executable.

---

## **Installation**

pip install gui_utilities

---

## **Update**

pip install -U gui_utilities