from typing import Optional, Iterable, List, Dict
from enum import Enum, unique
from datetime import datetime

from .rest import request_json, key_from_url
from .cache import cached, Requested


@unique
class Title(Enum):
    GM = 'GM'
    WGM = 'WGM'
    IM = 'IM'
    WIM = 'WIM'
    FM = 'FM'
    WFM = 'WFM'
    NM = 'NM'
    WNM = 'WNM'
    CM = 'CM'
    WCM = 'WCM'


@unique
class Status(Enum):
    CLOSED = 'closed'
    CLOSED_FAIR_PLAY = 'closed:fair_play_violations'
    BASIC = 'basic'
    PREMIUM = 'premium'
    MOD = 'mod'
    STAFF = 'staff'


class ClubActivity(object):
    club: 'Club'
    joined: datetime
    last_activity: datetime

    def __init__(self, club, joined, last_activity):
        self.club = club
        self.joined = joined
        self.last_activity = last_activity


class RatingStats(object):
    # Current stats
    category: str
    date: datetime
    rating: int
    rd: int
    # Best stats
    best_date: datetime
    best_rating: int
    # best_game: Game
    # Record
    wins: int
    losses: int
    draws: int
    time_per_move: int
    timeout_percent: float

    def __init__(self, category: str, d: dict):
        """Initialize from JSON dictionary."""
        self.category = category
        """Category of this rating."""

        self.date = datetime.fromtimestamp(d['last']['date'])
        self.rating = d['last']['rating']
        self.rd = d['last']['rd']

        # self.best_date = datetime.fromtimestamp(d['best']['date'])
        # self.best_rating = d['best']['rating']

        self.wins = d['record']['win']
        self.losses = d['record']['loss']
        self.draws = d['record']['draw']


@cached
class Player(object):
    # Profile properties
    url: Requested[str]
    username: Requested[str]
    original_username: Requested[str]
    player_id: Requested[int]
    title: Requested[Optional[Title]]
    status: Requested[Status]
    name: Requested[Optional[str]]
    avatar: Requested[Optional[str]]
    location: Requested[Optional[str]]
    country: Requested['Country']
    joined: Requested[datetime]
    last_online: Requested[datetime]
    followers: Requested[int]
    is_streamer: Requested[bool]
    # TODO: Report that `twitch_url` is optional
    twitch_url: Requested[Optional[str]]

    # Club properties
    clubs: Requested[List['Club']]
    _activity: Requested[Dict[str, ClubActivity]]

    # Stats properties
    _stats: Requested[Dict[str, RatingStats]]

    # Online properties
    is_online: Requested[bool]

    def __init__(self, key):
        self.key = key

        def profile_request():
            self._profile_request()

        self.url = Requested(profile_request)
        """URL of the Player's profile page."""

        self.username = Requested(profile_request)
        """Username of this player."""

        self.original_username = Requested(profile_request)
        """Capitalization-preserved username of this player."""

        self.player_id = Requested(profile_request)
        """User ID."""

        self.title = Requested(profile_request)
        """Optional title."""

        self.status = Requested(profile_request)
        """Status."""

        self.name = Requested(profile_request)
        """Optional name."""

        self.avatar = Requested(profile_request)
        """Optional URL to avatar (200x200 image)."""

        self.location = Requested(profile_request)
        """Optional location."""

        self.country = Requested(profile_request)
        """Country of the player"""

        self.joined = Requested(profile_request)
        """Timestamp of registration on Chess.com."""

        self.last_online = Requested(profile_request)
        """Timestamp of the most recent login."""

        self.followers = Requested(profile_request)
        """The number of players tracking this player's activity."""

        self.is_streamer = Requested(profile_request)
        """If the member is a Chess.com streamer."""

        self.twitch_url = Requested(profile_request)
        """Twitch.tv URL."""

        def club_request():
            self._club_request()

        self.clubs = Requested(club_request)
        """List of clubs the player is a member of."""

        self._activity = Requested(club_request)

        def stats_request():
            self._stats_request()

        self._stats = Requested(stats_request)

        def online_request():
            self._online_request()

        self.is_online = Requested(online_request, ttl=300)

    def _club_request(self):
        d = request_json(f"player/{self.key}/clubs")

        def get_activity(d):
            return ClubActivity(club=Club(key_from_url(d['url'])),
                                joined=datetime.fromtimestamp(d['joined']),
                                last_activity=datetime.fromtimestamp(
                                    d['last_activity']))

        activity = list(map(get_activity, d['clubs']))
        self._activity.receive({a.club.key: a for a in activity})
        self.clubs.receive(list(map(lambda a: a.club, activity)))

    def joined_club(self, key: str) -> Optional[datetime]:
        """Timestamp of joining club."""
        activity = self._activity().get(key)
        if activity:
            return activity.joined
        else:
            return None

    def last_active_in_club(self, key: str) -> Optional[datetime]:
        """Timestamp for last activity in club."""
        activity = self._activity().get(key)
        if activity:
            return activity.last_activity
        else:
            return None

    def _profile_request(self):
        d = request_json(f"player/{self.key}")
        self.url.receive(d['url'])
        self.username.receive(d['username'])
        self.original_username.receive(key_from_url(d['url']))
        self.player_id.receive(d['player_id'])
        self.title.receive(d.get('title', None))
        self.status.receive(Status(d['status']))
        self.name.receive(d.get('name', None))
        self.avatar.receive(d.get('avatar', None))
        self.location.receive(d.get('location', None))
        self.country.receive(Country(key_from_url(d['country'])))
        # TODO: Investigate time zone
        self.joined.receive(datetime.fromtimestamp(d['joined']))
        self.last_online.receive(datetime.fromtimestamp(d['last_online']))
        self.followers.receive(d['followers'])
        self.is_streamer.receive(d['is_streamer'])
        self.twitch_url.receive(d.get('twitch_url', None))

    def _stats_request(self):
        d = request_json(f"player/{self.key}/stats")
        categories = {}
        for category in d.keys():
            categories[category] = RatingStats(category, d[category])
        self._stats.receive(categories)

    def rating(self, category: str) -> Optional[int]:
        stats = self._stats()
        if category not in stats:
            return None

        return stats[category].rating

    def _online_request(self):
        d = request_json(f"player/{self.key}/is-online")
        self.is_online.receive(d['online'])


def titled_players(title: Title) -> Iterable[Player]:
    d = request_json(f"titled/{title.value}")
    return map(Player, d['players'])


def lookup_player(key: str) -> Player:
    return Player(key)


from .country import Country
from .club import Club
