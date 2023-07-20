from RequestHandler import *


class OpeningTree:
    start_name = "Start"
    move: str
    children: list

    def __init__(self, move=start_name):
        self.move = move
        self.children = []

    def add_node(self, new_node):
        self.children.append(new_node)

    def __str__(self, level=0):
        """String representation of the tree."""
        if level == 0:
            ret = self.start_name + "\n"
        else:
            ret = "|   " * (level - 1) + "|-- " + repr(self.move) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret


def recursive_tree_search(number_of_lines: int, recursion_depth: int,
                          list_of_played_moves: list[str] = None) -> OpeningTree:
    """

    :param number_of_lines: The number of most common move options to be considered
    :param recursion_depth: The length of each sequence
    :param list_of_played_moves: List of moves played in UCI format in order
    :return: Matrix of most common moves per line
    """
    if list_of_played_moves is None:
        # first level of recursion, initialize move list and tree data structure
        list_of_played_moves = []
        tree = OpeningTree()
    else:
        last_move = list_of_played_moves[len(list_of_played_moves) - 1]
        tree = OpeningTree(last_move)

    if recursion_depth <= 0:
        return tree

    # request next batch of most common moves
    json = make_request(number_of_lines=number_of_lines, played=list_of_played_moves)
    most_common_moves = get_most_common_moves(json)

    # recursively repeat the process for each of the next best moves
    for move in most_common_moves:
        new_line = list_of_played_moves.copy()
        new_line.append(move)
        resulting_move_tree = recursive_tree_search(number_of_lines, recursion_depth - 1, new_line)
        tree.add_node(resulting_move_tree)
    return tree


if __name__ == "__main__":
    lines = recursive_tree_search(2, 3)
    print(str(lines))
