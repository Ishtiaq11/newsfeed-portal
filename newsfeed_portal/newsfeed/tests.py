from django.test import TestCase

from .utils import get_top_headlines


class TestUtils(TestCase):
    def test_get_top_headlines(self):
        headlines = get_top_headlines(country="us")
        assert isinstance(headlines, list)
        headlines = get_top_headlines(q="Tesla")
        assert isinstance(headlines, list)
        headlines = get_top_headlines(sources="nbc-news")
        assert isinstance(headlines, list)
