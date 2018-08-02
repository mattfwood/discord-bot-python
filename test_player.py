import pytest
from time import time
from player import Player

@pytest.fixture(scope="module")
def smtp_connection():
    yield smtp_connection  # provide the fixture value
    print("teardown smtp")
    player = Player('test-player')
    player.delete_player()

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
    player.items['Nightmare Sword'] = 1
    player.update_player()
    assert 'Nightmare Sword' in player.items
