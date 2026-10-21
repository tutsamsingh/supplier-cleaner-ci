"""
Cleaning logic for messy supplier records.

This file has no web or database code, so it's easy to unit test.
"""

from datetime import datetime

# Date formats we accept. We try each one until one works.
DATE_FORMATS = [
    "%Y-%m-%d",    # 2026-10-20
    "%m/%d/%Y",    # 10/20/2026
    "%d-%b-%Y",    # 20-Oct-2026
    "%B %d, %Y",   # October 20, 2026
]


def clean_name(name):
    """Remove extra spaces and use Title Case: '  acme   ROCKET co ' -> 'Acme Rocket Co'."""
    if not name:
        return None
    return " ".join(name.split()).title()


def clean_email(email):
    """Trim spaces and lowercase: ' Sales@ACME.com ' -> 'sales@acme.com'."""
    if not email:
        return None
    return email.strip().lower()


def clean_price(price):
    """Turn '$1,200.50' into 1200.5. Returns None if it can't be read as a number."""
    if price is None:
        return None
    text = str(price).replace("$", "").replace(",", "").strip()
    try:
        return round(float(text), 2)
    except ValueError:
        return None


def clean_date(date_text):
    """Turn any accepted date format into 'YYYY-MM-DD'. Returns None if no format matches."""
    if not date_text:
        return None
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(date_text.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue  # try the next format
    return None


def clean_record(raw):
    """Clean every field of one supplier record (a dict) and return a new dict."""
    return {
        "name": clean_name(raw.get("name")),
        "email": clean_email(raw.get("email")),
        "price": clean_price(raw.get("price")),
        "date": clean_date(raw.get("date")),
    }
