# Python API and GraphQL Bridge for the [Chess.com Public API][PublicAPI]

An attempt to illustrate the benefits of using GraphQL instead of the current REST API for the [Chess.com Public API][PublicAPI].

The bridge also be used as a data source for tools that use GraphQL, such as building a static website using [GatsbyJS].

Includes a (hopefully) simple to use Python API for accessing the current API.

Since this was written as a quick demo, it does not support everything in the API, and can be a bit rough around the edges still. It is easy to extend however, and if there is interest, the bridge and the Python API can be split into proper packages of their own.

## Installation

Since this written mainly as a proof-of-concept, I haven't put any effort in packaging this up, so for now, just clone the repository, install requirements per below, and (if needed) add the directory to your `$PYTHONPATH`.

It needs at least Python 3.6 (eg., from the [Anaconda][Anaconda] distribution).

For using the API package only, you only need to install the [`requests`][Requests] package.

For running the `example.py` file, apart from the requirements for using the API, you also need to install the [`pandas`][Pandas], [`matplotlib`][Matplotlib], and [`click`][Click] packages.

The GraphQL bridge has the same requirements as the API package, plus the [`graphene`][Graphene], [`flask`][Flask], and [`flask_graphql`][FlaskGraphQL] packages.

Assuming that you have Python installed using [Anaconda][Anaconda], it could look something like this (on a Unix system) — assuming you want to create a new environment, which is usually recommended: 

```
# Cloning the repository
git clone https://github.com/chrka/chesscom-api-and-graphql-bridge
cd chesscom-api-and-graphql-bridge

# Create a new environment
conda create --name chesscom-graphql
source activate chesscom-graphql

# Install requirements for the API
conda install requests

# Install requirements for the example
conda install pandas matplotlib click

# Install requirements for the GraphQL bridge (not all in base conda)
conda install flask
pip install graphene Flask-GraphQL
```


## Usage

### Running the GraphQL bridge

```
# Make sure the chesscom and cqlbridge packages are available
export PYTHONPATH=<REPOSITORY_PATH>:$PYTHONPATH
python -m cqglbridge
```

And now you should be able to try it out in your browser [here](http://127.0.0.1:5000/graphql).


### Running the rating distribution example

```
cd <REPOSITORY_PATH>
python example.py chess-com-developer-community
```


## Python API (`import chesscom`)

**`lookup_player(username)`**: Returns a `Player` object for the user with the given username (case-insensitive).

**`titled_players(title)`**: Returns a list of `Player` objects for users with the given title (as an element of the `Title` enum).

**`lookup_club(key)`**: Returns a `Club` object for the club with the given key (case-insensitive). (The key is the last component of the Club's URL. Eg., The key for the _Chess.com Developer Community_-club with URL `https://www.chess.com/club/chess-com-developer-community´ is `chess-com-developer-community`.)

**`lookup_club(code)`**: Returns a `Country` object for the country with  the given 2-character ISO 3166 code (upper-case).


### Notes

* In general no checks are made to see if entities actually exist; doing so would take an API call which we in many cases can omit. 
* Properties are fetched lazily when requested. However, fetching the value of one property can often result in several other properties being filled is well due to how the Public API works.
* Although `Club`s and `Player`s have unique (numeric) IDs, the API generally uses names for these which can change. Unfortunately there does not seem to be any way to look up names from IDs some care has to be taken if you want to store historical data.
* Most properties are cached for 2 hours, the exception being `Player.is_online()` which expires after 5 minutes.



### class `Player`

Represents a member of Chess.com.

| Property                 | Description                                                                                           |  
| ------------------------ | ----------------------------------------------------------------------------------------------------- |  
| url()                    | URL of the Player's profile page                                                                      |  
| username()               | Username (per the API, generally lower-case)                                                          |  
| original_username()      | Capitalization-preserved username                                                                     |  
| player_id()              | Unique user ID                                                                                        |  
| title()                  | (Optional) Title (enum `Title`)                                                                       |  
| status()                 | Account status (enum `Status`)                                                                        |  
| name()                   | (Optional) Name                                                                                       |  
| avatar()                 | (Optional) URL to avatar (as 200x200 image)                                                           |  
| location()               | (Optional) Location                                                                                   |  
| country()                | Country                                                                                               |  
| joined()                 | Timestamp of registration on Chess.com (timezone?)                                                    |  
| last_online()            | Timestamp of most recent login (timezone?)                                                            |  
| followers()              | Number of players tracking this player's activity                                                     |  
| is_streamer()            | If the member is a Chess.com streamer                                                                 |  
| twitch_url()             | (Optional) URL to streamer's twitch stream                                                            |  
| clubs()                  | List of clubs the player is a member of                                                               |  
| is_online()              | If the player has been active in the last five minutes                                                |  
| rating(category)         | Rating for the given category (eg., `'chess_blitz'`, `'chess960_daily'` — see official documentation) |  
| joined_club(key)         | Timestamp of joining club with given key                                                              |  
| last_active_in_club(key) | Timestamp of latest activity in club with given key                                                   |  


### class `Club`.

Represents a club in Chess.com

| Property        | Description                                 |  
| --------------- | ------------------------------------------- |  
| key             | Key for this club                           |  
| name()          | Human-readable name                         |  
| club_id()       | Unique ID                                   |  
| icon()          | (Optional) URL to 200x200 image             |  
| country()       | Country associated with the club            |  
| created()       | Timestamp of creation                       |  
| last_activity() | Timestamp of most recent, post, match, etc. |  
| visibility()    | If the club is public or private            |  
| join_request()  | URL to submit a request to join the club    |  
| admin()         | List of admins of the club                  |  
| description()   | Description of the club                     |  
| members()       | List of the members of the club             |  


### class `Country`

Represents a country.

| Property | Description |
| --- | ---- |
| name() | Human-readable name |
| code() | ISO-31661-1 2-character code. |
| players() | List of active players in this country |
| clubs() | List of clubs associated with this country |


### enum `Title`

| Value | Description                |  
| ----- | -------------------------- |  
| GM    | Grandmaster                |  
| WGM   | Woman Grandmaster          |  
| IM    | International Master       |  
| WIM   | Woman International Master |  
| FM    | FIDE Master                |  
| WFM   | Woman FIDE Master          |  
| CM    | Candidate Master           |  
| WCM   | Woman Candidate Master     |  
| NM    | National Master            |  
| WNM   | Woman National Master      |  


### enum `Status`

| Value            | Description                               |  
| ---------------- | ----------------------------------------- |  
| CLOSED           | Closed Account                            |  
| CLOSED_FAIR_PLAY | Closed due to Fair Play Violation         |  
| BASIC            | Basic Account                             |  
| PREMIUM          | Premium Account (Gold, Platinum, Diamond) |  
| MOD              | Moderator Account                         |  
| STAFF            | Staff Account                             |  


## GraphQL Schema

```graphql
schema {
  query: Query
}

type Club {
  key: String!
  name: String!
  clubId: Int!
  icon: String
  country: Country!
  created: DateTime!
  lastActivity: DateTime!
  joinRequest: String!
  admin: [Player!]!
  description: String
  members: [Player!]!
}

type Country {
  name: String!
  code: String!
  players: [Player!]!
  clubs: [Club!]!
}

scalar DateTime

type Player {
  url: String!
  username: String!
  playerId: Int!
  title: Title
  status: Status!
  name: String
  avatar: String
  location: String
  country: Country!
  joined: DateTime!
  lastOnline: DateTime!
  followers: Int!
  isStreamer: Boolean!
  twitchUrl: String
  clubs: [Club!]!
  joinedClub(key: String): DateTime
  lastActiveInClub(key: String): DateTime
  rating(category: String): Int
  isOnline: Boolean!
}

type Query {
  player(username: String): Player
  titledPlayers(title: Title): [Player!]
  club(key: String): Club
  country(code: String): Country
}

enum Status {
  CLOSED
  CLOSED_FAIR_PLAY
  BASIC
  PREMIUM
  MOD
  STAFF
}

enum Title {
  GM
  WGM
  IM
  WIM
  FM
  WFM
  NM
  WNM
  CM
  WCM
}
```


[PublicAPI]: https://www.chess.com/news/view/published-data-api
[GatsbyJS]: https://www.gatsbyjs.org
[Requests]: http://www.python-requests.org/
[Pandas]: https://pandas.pydata.org
[Matplotlib]: https://matplotlib.org
[Click]: https://click.palletsprojects.com
[Graphene]: https://graphene-python.org
[Flask]: http://flask.pocoo.org
[FlaskGraphQL]: https://github.com/graphql-python/flask-graphql
[Anaconda]: https://www.anaconda.com
