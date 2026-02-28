import re

def decimal_format(number, decimals = None):
    if isinstance(number, float) and number.is_integer(): number = int(number)
    if decimals is not None:
        formated_number = f"{number:,.{decimals}f}"
        if "." in formated_number: formated_number = formated_number.rstrip("0").rstrip(".")
    else: formated_number = f"{number:,}"
    return formated_number.replace(",", "X").replace(".", ",").replace("X", ".")

def datetime_format(datetime, include_year = True, include_time = True, include_second = True):
    day = datetime.day
    month = datetime.month
    year = decimal_format(datetime.year)
    hour = getattr(datetime, "hour", 0)
    minute = getattr(datetime, "minute", 0)
    second = getattr(datetime, "second", 0)
    if include_time: include_time = (hour != 0 or minute != 0 or second != 0)
    if include_second: include_second = (second != 0)
    date = f"{day:02d}/{month:02d}"
    if include_year: date += f"/{year}"
    if include_time:
        time = f"{hour:02d}:{minute:02d}"
        if include_second: time += f":{second:02d}"
        return f"{date} - {time}"
    return date

def id_format(id):
    if "." in id: return id
    elif len(id) == 8: return f"{id[0:2]}.{id[2:5]}.{id[5:8]}"
    elif len(id) == 7: return f"{id[0:1]}.{id[1:4]}.{id[4:7]}"

def cellphone_number_format(cellphone_number):
    formated_cellphone_number = "".join(filter(str.isdigit, str(cellphone_number)))
    return f"{formated_cellphone_number[0:4]} - {formated_cellphone_number[4:10]}"

def html_expression_format(expression):
    html_expression = expression
    html_expression = re.sub(
        r"\\frac\{(.*?)\}\{(.*?)\}", r"""<span style = "white-space: normal;">\1⁄\2</span>""",
        html_expression
    )
    html_expression = re.sub(r"_\{([^}]+)\}", r"<sub>\1</sub>", html_expression)
    html_expression = re.sub(r"\^\{([^}]+)\}", r"<sup>\1</sup>", html_expression)
    html_expression = re.sub(r"_([a-zA-Z0-9]+)", r"<sub>\1</sub>", html_expression)
    html_expression = re.sub(r"\^([a-zA-Z0-9]+)", r"<sup>\1</sup>", html_expression)
    return html_expression

def convert_to_double(number): return float(str(number).replace(".", "").replace(",", "."))

def define_equality_symbol(number, number_rounded): return "=" if number == number_rounded else "≅"