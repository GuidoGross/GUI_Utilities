import re
import requests
from datetime import datetime
from .dialogs import information_message_box
from .system import _resource_path

TLDS_LIST = _resource_path("tlds/tlds.txt")

_email_pattern = None

def _get_tlds():
    url = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
    try:
        response = requests.get(url, timeout = 10)
        response.raise_for_status()
        tlds = [tld.lower() for tld in response.text.splitlines()[1:] if tld]
        if tlds: _export_tlds(tlds)
        return tlds
    except requests.RequestException: return _import_tlds()

def _import_tlds():
    try:
        with open(TLDS_LIST, "r", encoding = "utf-8") as saved_tlds:
            return [tld.strip() for tld in saved_tlds]
    except FileNotFoundError: return []

def _export_tlds(tlds):
    try:
        with open(TLDS_LIST, "w", encoding = "utf-8") as saved_tlds:
            saved_tlds.write("\n".join(tlds))
    except IOError: pass

def _build_email_pattern():
    global _email_pattern
    if _email_pattern is not None: return _email_pattern
    tlds = _get_tlds()
    if tlds: tld_pattern = "|".join(sorted(tlds, key = len, reverse = True))
    else: tld_pattern = r"[a-zA-Z]{2,63}"
    _email_pattern = re.compile(
        r"^(?P<local>[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+"
        r"(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*)@"
        r"(?P<dominio>(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
        r"(?:" + tld_pattern + r"))$",
        re.IGNORECASE
    )
    return _email_pattern

def check_if_list_is_empty(list, blank_error = "La lista está vacía"):
    if not list:
        information_message_box(blank_error)
        return True
    return False

def validate_option(
    options,
    selection,
    invalid_error = "La opción ingresada no es válida, intente nuevamente",
):
    if selection.upper() in options: return selection.upper()
    information_message_box(invalid_error)

def validate_string(
    string,
    blank_error = "El texto no puede estar vacío, intente nuevamente"
):
    if string: return string
    information_message_box(blank_error)

def validate_integer(
    integer,
    blank_error = "El número no puede estar vacío",
    invalid_error = "El número ingresado no es válido, intente nuevamente"
):
    if not integer:
        information_message_box(blank_error)
        return
    pattern = re.compile(r"^(?:\d{1,3}(?:\.\d{3})*|\d+)$")
    if pattern.match(integer):
        unformatted_integer = integer.replace(".", "")
        return int(unformatted_integer)
    information_message_box(invalid_error)

def validate_double(
    double,
    blank_error = "El número no puede estar vacío",
    invalid_error = "El número ingresado no es válido, intente nuevamente"
):
    if not double:
        information_message_box(blank_error)
        return
    pattern = re.compile(r"^(?:\d{1,3}(?:\.\d{3})*|\d+)(?:,(\d{1,2}))?$")
    if pattern.match(double):
        unformatted_double = double.replace(".", "").replace(",", ".")
        return float(unformatted_double)
    information_message_box(invalid_error)

def validate_datetime(
    datetime,
    blank_error = "La fecha no puede estar vacía",
    invalid_error = "La fecha ingresada no es válida, intente nuevamente",
    include_year = True,
    include_time = True,
    include_second = True
):
    if not datetime:
        information_message_box(blank_error)
        return
    date = r"(0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])"
    if include_year: date += r"/(\d{4}|\d{1,2}\.\d{3})"
    time = r"([01]\d|2[0-3]):[0-5]\d"
    if include_second: time += r"(?::[0-5]\d)?"
    pattern = rf"^{date}(?: - {time})?$" if include_time else rf"^{date}$"
    if re.match(pattern, datetime):
        cleaned_datetime = datetime.replace(".", "")
        if " - " in cleaned_datetime:
            if cleaned_datetime.count(":") == 2:
                format = "%d/%m/%Y - %H:%M:%S" if include_year else "%d/%m - %H:%M:%S"
            else: format = "%d/%m/%Y - %H:%M" if include_year else "%d/%m - %H:%M"
        else: format = "%d/%m/%Y" if include_year else "%d/%m"
        return datetime.strptime(cleaned_datetime, format)
    information_message_box(invalid_error)

def validate_id(
    id,
    blank_error = "El número de D.N.I. no puede estar vacío",
    invalid_error = "El número de D.N.I. ingresado no es válido, intente nuevamente"
):
    if not id:
        information_message_box(blank_error)
        return
    pattern = re.compile(r"^(?:\d{8}|(?:\d{1,2}\.\d{3}\.\d{3}))$")
    if pattern.match(id): return id
    information_message_box(invalid_error)

def validate_cellphone_number(
    cellphone_number,
    blank_error = "El número telefónico no puede estar vacío",
    invalid_error = "El número telefónico ingresado no es válido, intente nuevamente"
):
    if not cellphone_number:
        information_message_box(blank_error)
        return
    pattern = re.compile(r"^\d{4}\s*-?\s*\d{6}$")
    if pattern.match(cellphone_number): return cellphone_number
    information_message_box(invalid_error)

def validate_email(
    email,
    blank_error = "El correo electrónico no puede estar vacío",
    invalid_error = "El correo electrónico ingresado no es válido, intente nuevamente"
):
    if not email:
        information_message_box(blank_error)
        return
    pattern = _build_email_pattern()
    if pattern.match(email): return email
    information_message_box(invalid_error)