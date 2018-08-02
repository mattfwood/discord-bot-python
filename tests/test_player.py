import pytest
from time import time
from .context import Player

def test_create_player():
    player = Player('test-player')
    # Should have default values
    assert player.discord_id == 'test-player'
    assert player.items == {}
    assert player.points == 1

def test_update_points():
    player = Player('test-player')
    player.update_points(500)
    assert player.points == 501

def test_add_item():
    player = Player('test-player')
    assert player.has_item('Nightmare Sword') is False
    player.items['Nightmare Sword'] = 1
    player.update_player()
    assert player.has_item('Nightmare Sword') is True
    assert 'Nightmare Sword' in player.items
    assert player.items['Nightmare Sword'] == 1

def test_increment_item():
    player = Player('test-player')
    assert 'Nightmare Sword' in player.items
    assert player.has_item('Nightmare Sword') is True
    player.items['Nightmare Sword'] += 1
    player.update_player()
    assert player.items['Nightmare Sword'] == 2

