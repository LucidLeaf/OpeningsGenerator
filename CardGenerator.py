import chess
import chess.svg
import genanki

import OpeningTree

DECK_NAME = "Generated Chess Openings"
DECK_ID = 2059416610
MODEL_NAME = "Opening Continuations"
MODEL_ID = 1607392319

FIELD_NAMES = [
    'Position FEN',
    'Position Name',
    'Position Image',
    'Continuation Names',
    'Continuation FENs',
    'Continuation Images'
]

# Define the model (note type)
model = genanki.Model(
    MODEL_ID,  # An arbitrary model ID (must be unique)
    MODEL_NAME,
    fields=[{'name': FIELD_NAMES[0]},
            {'name': FIELD_NAMES[1]},
            {'name': FIELD_NAMES[2]},
            {'name': FIELD_NAMES[3]},
            {'name': FIELD_NAMES[4]},
            {'name': FIELD_NAMES[5]}]
)

# Create the deck
deck = genanki.Deck(
    DECK_ID,  #
    DECK_NAME
)


class OpeningNote(genanki.Note):
    # Use fen as id
    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])


def write_fen_to_svg_file(fen: str) -> str:
    # convert fen to svg
    board = chess.Board(fen)
    svg_board = chess.svg.board(board=board)
    # write svg to file
    filename = fen.split(" ")[0].replace("/", "") + ".svg"
    with open(filename, "w") as file:
        file.write(svg_board)
    return filename


if __name__ == "__main__":
    fen = OpeningTree.generate_opening_tree(1, 3).children[0].children[0].children[0].fen
