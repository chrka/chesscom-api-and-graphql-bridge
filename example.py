import pandas as pd
import matplotlib.pyplot as plt
import chesscom
import click


def plot_club_rating_distribution(club_key):
    club = chesscom.lookup_club(club_key)
    ratings = pd.DataFrame([{
        'bullet': member.rating('chess_bullet'),
        'blitz': member.rating('chess_blitz'),
        'rapid': member.rating('chess_rapid')
    } for member in club.members()])
    ratings.plot(kind='density')
    plt.title(f"Rating Distribution of {club.name()}")
    plt.xlabel('Rating')
    plt.show()


@click.command()
@click.argument('club')
def main(club):
    plot_club_rating_distribution(club)


if __name__ == '__main__':
    main()
