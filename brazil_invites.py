# Example file for https://www.chess.com/clubs/forum/view/automated-club-invites
# (Could do with a bit more abstraction =)

import chesscom
import datetime
import logging

# Set level=logging.DEBUG to see API requests
logging.basicConfig(level=logging.INFO)


def read_invited(filename="invited.txt"):
    try:
        with open(filename, "r") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return []


def append_invited(players, filename="invited.txt"):
    with open(filename, "a+") as f:
        for player in players:
            f.write(player.username() + '\n')


def is_premium(player):
    return player.status() in [chesscom.Status.PREMIUM, chesscom.Status.MOD,
                               chesscom.Status.STAFF]


def is_potential_invite(player):
    # Check that player's account is older than one month (30 days)
    if datetime.datetime.today() - player.joined() < datetime.timedelta(
            days=30):
        logging.info("%s's account is too young", player.username())
        return False

    # Check that player has a name with at least both a first and last name
    if not player.name() or len(player.name().split(' ')) < 2:
        logging.info("%s does not have a full name (%s)", player.username(),
                     player.name())
        return False

    # Check that player has an avatar or is premium
    if not player.avatar() and not is_premium(player):
        logging.info("%s does not have an avatar or is not premium",
                     player.username())
        return False

    logging.info("%s is a potential invite", player.username())
    return True


if __name__ == '__main__':
    inviteds = read_invited()
    print(inviteds)
    new_inviteds = []

    # Get and filter Brazilian players
    brazil = chesscom.lookup_country('BR')
    for player in brazil.players():
        if player.username() in inviteds:
            print("User {} found".format(player.username()))
        if player.username() not in inviteds and is_potential_invite(player):
            new_inviteds.append(player)

    # Display potential invites
    for player in new_inviteds:
        print(player.url())

    # Save new invites to "invited.txt"
    append_invited(new_inviteds)
