from RequestHandler import *


class OpeningTree:
    start_name = "Start"
    move: str
    name: str
    fen: str
    children: list

    def __init__(self, fen, move=start_name, name=""):
        self.move = move
        self.name = name
        self.fen = fen
        self.children = []

    def add_node(self, new_node):
        self.children.append(new_node)

    def find_path_to_move(self, target_move, current_path=None):
        """Find the path to the target move in the tree."""
        if current_path is None:
            current_path = []
        if self.move != self.start_name:
            current_path = current_path + [self.move]

        if self.move == target_move:
            return current_path

        for child in self.children:
            found_path = child.find_path_to_move(target_move, current_path)
            if found_path:
                return found_path

        return None

    def __str__(self, level=0):
        """String representation of the tree."""
        ret = "|   " * level + "|-- " + self.move + ": " + self.name + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret


def generate_opening_tree(number_of_lines: int, recursion_depth: int,
                          list_of_played_moves: list[str] = None) -> OpeningTree:
    """

    :param number_of_lines: The number of most common move options to be considered
    :param recursion_depth: The length of each sequence
    :param list_of_played_moves: List of moves played in UCI format
    :return: Matrix of most common moves per line
    """
    if list_of_played_moves is None:
        list_of_played_moves = []

    # request information about position
    position_information = retrieve_position_information(number_of_lines=number_of_lines, played=list_of_played_moves)

    if not list_of_played_moves:
        tree = OpeningTree(position_information.fen)
    else:
        last_move = list_of_played_moves[len(list_of_played_moves) - 1]
        tree = OpeningTree(move=last_move, fen=position_information.fen, name=position_information.name)

    if recursion_depth <= 0:
        return tree

    # recursively repeat the process for each of the next best moves
    for move in position_information.common_moves:
        new_line = list_of_played_moves.copy()
        new_line.append(move)
        resulting_move_tree = generate_opening_tree(number_of_lines, recursion_depth - 1, new_line)
        tree.add_node(resulting_move_tree)
    return tree
