"""Unit tests for the cleaning logic. These don't need a database."""

from app.cleaner import clean_date, clean_email, clean_name, clean_price, clean_record


def test_clean_name_removes_extra_spaces_and_fixes_case():
    assert clean_name("  acme   ROCKET co ") == "Acme Rocket Co"


def test_clean_email_lowercases_and_trims():
    assert clean_email(" Sales@ACME.com ") == "sales@acme.com"


def test_clean_price_handles_dollar_signs_and_commas():
    assert clean_price("$1,200.50") == 1200.5


def test_clean_price_returns_none_for_bad_input():
    assert clean_price("call for quote") is None


def test_clean_date_accepts_different_formats():
    assert clean_date("10/20/2026") == "2026-10-20"
    assert clean_date("20-Oct-2026") == "2026-10-20"
    assert clean_date("October 20, 2026") == "2026-10-20"


def test_clean_record_cleans_every_field():
    raw = {
        "name": " orbital   PARTS inc",
        "email": "BUY@Orbital.io ",
        "price": "$99",
        "date": "2026-01-05",
    }
    assert clean_record(raw) == {
        "name": "Orbital Parts Inc",
        "email": "buy@orbital.io",
        "price": 99.0,
        "date": "2026-01-05",
    }
