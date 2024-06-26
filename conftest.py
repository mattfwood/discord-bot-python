from player import Player


def pytest_configure(config):
    import sys

    sys._called_from_test = True


def pytest_unconfigure(config):
    import sys

    del sys._called_from_test
    player = Player('test-player')
    player.delete_player()
