import graphene
import chesscom

Title = graphene.Enum.from_enum(chesscom.Title)
Status = graphene.Enum.from_enum(chesscom.Status)


class Player(graphene.ObjectType):
    url = graphene.String(required=True)

    def resolve_url(self, info):
        return self.url()

    username = graphene.String(required=True)

    def resolve_username(self, info):
        return self.original_username()

    player_id = graphene.Int(required=True)

    def resolve_player_id(self, info):
        return self.player_id()

    title = graphene.Field(Title)

    def resolve_title(self, info):
        return self.title()

    status = graphene.Field(Status, required=True)

    def resolve_status(self, info):
        return self.status()

    name = graphene.String()

    def resolve_name(self, info):
        return self.name()

    avatar = graphene.String()

    def resolve_avatar(self, info):
        return self.avatar()

    location = graphene.String()

    def resolve_location(self, info):
        return self.location()

    country = graphene.Field(lambda: Country, required=True)

    def resolve_country(self, info):
        return self.country()

    joined = graphene.DateTime(required=True)

    def resolve_joined(self, info):
        return self.joined()

    last_online = graphene.DateTime(required=True)

    def resolve_last_online(self, info):
        return self.last_online()

    followers = graphene.Int(required=True)

    def resolve_followers(self, info):
        return self.followers()

    is_streamer = graphene.Boolean(required=True)

    def resolve_is_streamer(self, info):
        return self.is_streamer()

    twitch_url = graphene.String()

    def resolve_twitch_url(self, info):
        return self.twitch_url()

    clubs = graphene.List(graphene.NonNull(lambda: Club), required=True)

    def resolve_clubs(self, info):
        return self.clubs()

    joined_club = graphene.DateTime(key=graphene.String())

    def resolve_joined_club(self, info, key):
        return self.joined_club(key)

    last_active_in_club = graphene.DateTime(key=graphene.String())

    def resolve_last_active_in_club(self, info, key):
        return self.last_active_in_club(key)

    rating = graphene.Int(category=graphene.String())

    def resolve_rating(self, info, category):
        return self.rating(category)

    is_online = graphene.Boolean(required=True)

    def resolve_is_online(self, info):
        return self.is_online()


class Club(graphene.ObjectType):
    key = graphene.String(required=True)

    def resolve_key(self, info):
        return self.key

    name = graphene.String(required=True)

    def resolve_name(self, info):
        return self.name()

    club_id = graphene.Int(required=True)

    def resolve_club_id(self, info):
        return self.club_id()

    icon = graphene.String()

    def resolve_icon(self, info):
        return self.icon()

    country = graphene.Field(lambda: Country, required=True)

    def resolve_country(self, info):
        return self.country()

    created = graphene.DateTime(required=True)

    def resolve_created(self, info):
        return self.created()

    last_activity = graphene.DateTime(required=True)

    def resolve_last_activity(self, info):
        return self.last_activity()

    join_request = graphene.String(required=True)

    def resolve_join_request(self, info):
        return self.join_request()

    admin = graphene.List(graphene.NonNull(Player), required=True)

    def resolve_admin(self, info):
        return self.admin()

    description = graphene.String()

    def resolve_description(self, info):
        return self.description()

    members = graphene.List(graphene.NonNull(Player), required=True)

    def resolve_members(self, info):
        return self.members()


class Country(graphene.ObjectType):
    name = graphene.String(required=True)

    def resolve_name(self, info):
        return self.name()

    code = graphene.String(required=True)

    def resolve_code(self, info):
        return self.code()

    players = graphene.List(graphene.NonNull(Player), required=True)

    def resolve_players(self, info):
        return self.players()

    clubs = graphene.List(graphene.NonNull(lambda: Club), required=True)

    def resolve_clubs(self, info):
        return self.clubs()


class Query(graphene.ObjectType):
    player = graphene.Field(Player, username=graphene.String())

    def resolve_player(self, info, username):
        return chesscom.lookup_player(username)

    titled_players = graphene.List(graphene.NonNull(Player), title=Title())

    def resolve_titled_players(self, info, title):
        return chesscom.titled_players(chesscom.Title(title))

    club = graphene.Field(Club, key=graphene.String())

    def resolve_club(self, info, key):
        return chesscom.lookup_club(key)

    country = graphene.Field(Country, code=graphene.String())

    def resolve_country(self, info, code):
        return chesscom.lookup_country(code)


schema = graphene.Schema(query=Query)
