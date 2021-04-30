import re
from datetime import datetime


def format_date(date):
    """Format the date to datetime string"""
    month, day, year = date.split("/")
    return datetime(int(year), int(month), int(day)).strftime(
        "%Y-%m-%dT%H:%M:%S%Z"
    )


def get_ajax_identifier(page_text):
    """Extract from raw HTML the AJAX identifier used in the POST request payload"""
    return (
        re.findall(r"\"ajaxIdentifier\":\".*?\"", page_text)[1]
        .split(":")[-1]
        .replace('"', "")
    )
