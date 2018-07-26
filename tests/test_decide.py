import os
import sys

from commands import decide

def test_standard():
    choices = '1, 2, 3'
    result = decide(choices, None)
    assert result in choices

def test_single():
    choices = '1'
    result = decide(choices, None)
    assert result in choices