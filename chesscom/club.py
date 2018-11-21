from typing import Optional, Iterable, List
from enum import Enum, unique
from datetime import datetime

from .rest import request_json, key_from_url
from .cache import cached, Requested


@cached
class Club(object):
    # Profile properties
    name: Requested[str]
    club_id: Requested[int]
    icon: Requested[str]
    country: Requested['Country']
    created: Requested[datetime]
    last_activity: Requested[datetime]
    visibility: Requested[bool]
    join_request: Requested[str]
    admin: Requested[List['Player']]
    description: Requested[Optional[str]]

    # Member properties
    members: Requested[List['Player']]

    def __init__(self, key):
        self.key = key

        def profile_request():
            self._profile_request()

        self.name = Requested(profile_request)
        """Human-readable name of this club."""

        self.club_id = Requested(profile_request)
        """Non-changing Chess.com ID of this club."""

        self.icon = Requested(profile_request)
        """Optional URL of a 200x200 image."""

        self.country = Requested(profile_request)
        """The club's country."""

        self.created = Requested(profile_request)
        """Timestamp of creation on Chess.com"""

        self.last_activity = Requested(profile_request)
        """Timestamp of the most recent post, match, etc."""

        self.visibility = Requested(profile_request)
        """Whether the club is public or private."""

        self.join_request = Requested(profile_request)
        """Location to submit a request to join this club."""

        self.admin = Requested(profile_request)
        """List of the club's admins."""

        self.description = Requested(profile_request)
        """Text description of the club."""

        def member_request():
            self._member_request()

        self.members = Requested(member_request)
        """Members of the club"""

    def _profile_request(self):
        def get_admin(s):
            return Player(key_from_url(s))

        d = request_json(f"club/{self.key}")
        self.name.receive(d['name'])
        self.club_id.receive(d['club_id'])
        self.icon.receive(d.get('icon', None))
        self.country.receive(Country(key_from_url(d['country'])))
        self.created.receive(datetime.fromtimestamp(d['created']))
        self.last_activity.receive(datetime.fromtimestamp(d['last_activity']))
        self.visibility.receive(d['visibility'])
        self.join_request.receive(d['join_request'])
        self.admin.receive(list(map(get_admin, d['admin'])))
        # TODO: Report that 'description' is not always present
        self.description.receive(d.get('description', None))

    def _member_request(self):
        d = request_json(f"club/{self.key}/members")
        members = []
        for timeframe in d.keys():
            members.extend(map(lambda x: Player(x['username']), d[timeframe]))
        self.members.receive(members)


def lookup_club(key: str) -> Club:
    return Club(key)


from .player import Player
from .country import Country
