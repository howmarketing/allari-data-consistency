from src.lib.helpers.format import normalize_phone

def test_normalize_phone():
    # Test case 1: Normal phone number with hyphens, parentheses, and spaces
    assert normalize_phone("(123) 456-7890") == "1234567890"

    # Test case 2: Normal phone number without any special characters
    assert normalize_phone("1234567890") == "1234567890"

    # Test case 3: Phone number with leading hyphens, parentheses, and spaces
    assert normalize_phone("-(123) 456-7890") == "1234567890"

    # Test case 4: Phone number with trailing hyphens, parentheses, and spaces
    assert normalize_phone("(123) 456-7890-") == "1234567890"

    # Test case 5: Empty phone number
    assert normalize_phone("") == None