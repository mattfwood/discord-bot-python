import re
import pytest
from commands import subreddit

is_url = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def test_subreddit():
    random_url = subreddit('overwatch', None)
    assert type(random_url) is str
    assert 'http' in random_url
    assert re.match(is_url, random_url)

def test_invalid():
    """
    Make sure that an invalid subreddit returns error message
    """
    result = subreddit('oeaifefnia', None)
    assert result == 'Subreddit not found', 'Returns an error message when an invalid subreddit is provided'
