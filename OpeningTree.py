from typing import List, Any

import RequestHandler
from RequestHandler import *


def recursive_tree_search(number_of_lines: int, recursion_depth: int, list_of_played_moves: list[str] = None) -> list:
    """

    :param number_of_lines: The number of most common move options to be considered
    :param recursion_depth: The length of each sequence
    :param list_of_played_moves: List of moves played in UCI format in order
    :return: Matrix of most common moves per line
    """
    if list_of_played_moves is None:
        list_of_played_moves = []
    if recursion_depth <= 0:
        return list_of_played_moves

    # request next batch of most common moves
    json = make_request(fen=initial_game_fen, played=list_of_played_moves, number_of_lines=number_of_lines)
    most_common_moves = get_most_common_moves(json)

    # recursively repeat the process for each of the next best moves
    decision_tree = []
    for move in most_common_moves:
        new_line = list_of_played_moves.copy()
        new_line.append(move)
        resulting_move_tree = recursive_tree_search(number_of_lines, recursion_depth - 1, new_line)
        decision_tree.append(resulting_move_tree)
    return decision_tree


if __name__ == "__main__":
    pprint(recursive_tree_search(2, 2))
