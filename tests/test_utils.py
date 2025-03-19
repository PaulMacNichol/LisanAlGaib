# tests/test_utils.py

import unittest
from utils.helpers import format_time, is_valid_url, sanitize_text


class TestHelpers(unittest.TestCase):
    def test_format_time_less_than_hour(self):
        # Test durations less than one hour.
        self.assertEqual(format_time(0), "00:00")
        self.assertEqual(format_time(59), "00:59")
        self.assertEqual(format_time(75), "01:15")
        self.assertEqual(format_time(60), "01:00")

    def test_format_time_more_than_hour(self):
        # Test durations that include hours.
        # 1 hour, 1 minute, 1 second
        self.assertEqual(format_time(3661), "01:01:01")
        self.assertEqual(format_time(3600), "01:00:00")   # exactly 1 hour

    def test_is_valid_url(self):
        # Valid URLs
        self.assertTrue(is_valid_url("http://example.com"))
        self.assertTrue(is_valid_url("https://example.com"))
        self.assertTrue(is_valid_url(
            "https://www.example.com/path?query=param"))
        # Invalid URLs
        self.assertFalse(is_valid_url("example.com"))
        self.assertFalse(is_valid_url("not a url"))
        self.assertFalse(is_valid_url(""))
        # Depending on your definition, ftp may be considered invalid.
        self.assertFalse(is_valid_url("ftp://example.com"))

    def test_sanitize_text(self):
        # Test removal of control characters and trimming.
        self.assertEqual(sanitize_text("Hello\x00 World"), "Hello World")
        self.assertEqual(sanitize_text("  Trim me  "), "Trim me")
        self.assertEqual(sanitize_text("Hello\x1FWorld"), "HelloWorld")
        self.assertEqual(sanitize_text("NoControlChars"), "NoControlChars")
        # Test when string contains only control characters.
        self.assertEqual(sanitize_text("\x00\x1F\x7F"), "")


if __name__ == "__main__":
    unittest.main()
