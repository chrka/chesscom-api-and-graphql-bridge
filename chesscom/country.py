import requests

from typing import Optional, List
from enum import Enum, unique
from datetime import datetime

from chesscom.rest import request_json, key_from_url
from .cache import cached, Requested


@cached
class Country(object):
    name: Requested[str]
    code: Requested[str]
    players: Requested[List['Player']]
    clubs: Requested[List['Club']]

    def __init__(self, key):
        # NB. key must be uppercase
        self.key = key

        def request_info():
            self._request_info()

        self.name = Requested(request_info)
        """The human-readable name of this country."""

        self.code = Requested(request_info)
        """ISO-31661-1 2-character code."""

        def request_players():
            self._request_players()

        self.players = Requested(request_players)
        """List of active players in this country."""

        def request_clubs():
            self._request_clubs()

        self.clubs = Requested(request_clubs)
        """List of clubs associated with this country."""

    def _request_info(self):
        d = request_json(f"country/{self.key}")
        self.name.receive(d['name'])
        self.code.receive(d['code'])

    def _request_players(self):
        d = request_json(f"country/{self.key}/players")
        self.players.receive(list(map(Player, d['players'])))

    def _request_clubs(self):
        d = request_json(f"country/{self.key}/clubs")

        def get_club(url):
            return Club(key_from_url(url))

        self.clubs.receive(list(map(get_club, d['clubs'])))


def lookup_country(key: str) -> Country:
    return Country(key)


from .club import Club
from .player import Player
