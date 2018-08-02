from player import Player

def pytest_unconfigure(config):
    player = Player('test-player')
    player.delete_player()