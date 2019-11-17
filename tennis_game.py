# coding=utf-8

import random


def initialize():
    # region Mise en oeuvre
    import logging
    import sys
    import locale
    import os

    logging.basicConfig(level="INFO")
    root_handlers = logging.root.handlers
    handler, = root_handlers
    # noinspection SpellCheckingInspection
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    locale.setlocale(locale.LC_ALL, "")
    return logger
    # endregion


logger = initialize()


def main():
    # noinspection PyShadowingNames
    from collections import namedtuple
    Player = namedtuple("Player", ("name", "point"))

    def play(command_line_configuration):
        def initialize():
            logger.info("Enter Le nom du premier joueur:")
            name_player_1 = input()
            logger.info("Enter Le nom du deuxième joueur:")
            name_player_2 = input()
            logger.info("Qui commence le premier service? 1 pour {}, 2 pour {}".format(name_player_1, name_player_2))
            play_first = int(input())
            while play_first not in (1, 2):
                logger.info("Valeur incorrecte Tapez 1 pour {}, 2 pour {}".format(name_player_1, name_player_2))
                play_first = int(input())
            name_player_1, name_player_2 = get_player_order(play_first, name_player_1, name_player_2)
            player1 = Player(name=name_player_1, point=0)
            player2 = Player(name=name_player_2, point=0)
            return player1, player2

        def get_player_order(play_first, player1, player2):
            if play_first == 2:
                player1 = player1 + player2
                player2 = player1[0: (len(player1) - len(player2))]
                player1 = player1[len(player2):]
            return player1, player2

        def get_server_result(player):
            points = player.point + random.randint(0, 1)
            player = player._replace(point=points)
            return player

        def max_point(player1, player2):
            if player1.point - player2.point == -1:
                return player2
            return player1

        player1, player2 = initialize()
        while True:
            rule = {0: 0, 1: 15, 2: 30, 3: 40, 4: 41}
            if rule[player1.point] == 40 and rule[
                player2.point] == 40 and command_line_configuration.deuce_rule:
                player1, player2 = initialize()
                avantage = False
                while True:
                    player1 = get_server_result(player1)
                    player2 = get_server_result(player2)
                    if player1.point - player2.point == 0:
                        break
                    elif not avantage:
                        avantage = True
                        logger.info("{player} a eu l'avantage".format(player=max_point(player1, player2).name))
                    else:
                        break
                    logger.info("{player} a gagné".format(player=max_point(player1, player2).name))

            player1 = get_server_result(player1)
            logger.info(
                "{player1} {score1} | {score2} {player2}".format(player1=player1.name, score1=rule[player1.point],
                                                                 score2=rule[player2.point], player2=player2.name))
            if rule[player1.point] <= 40:
                player2 = get_server_result(player2)
                logger.info(
                    "{player1} {score1} | {score2} {player2}".format(player1=player1.name, score1=rule[player1.point],
                                                                     score2=rule[player2.point], player2=player2.name))
                if rule[player2.point] > 40:
                    logger.info(
                        "Le joueur {name} a gagné ce match".format(name=player2.name))
                    exit(0)
            else:
                logger.info(
                    "Le joueur {name} a gagné ce match".format(name=player1.name))
                exit(0)

    def get_command_line_configuration():
        # region Mise en oeuvre
        def command_parser():
            """Je fournis l'analyseur de la ligne de commande.

            :return: l'analyseur
            :rtype: argparse.ArgumentParser
            """
            # region Mise en oeuvre
            import argparse

            parser = argparse.ArgumentParser(
                description="Test technique 'Manage Tennis Game' ",
                formatter_class=argparse.ArgumentDefaultsHelpFormatter
            )
            parser.add_argument(
                "--deuce_rule",
                help="User story choise",
                action="store_true",
                default=False
            )
            return parser
            # endregion

        command_parser = command_parser()
        configuration = command_parser.parse_args()
        return configuration
        # endregion

    command_line_configuration = get_command_line_configuration()
    play(command_line_configuration)


if __name__ == '__main__':
    main()
