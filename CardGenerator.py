import base64
from io import BytesIO

import cairosvg
import chess
import chess.svg
import genanki

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


def fen_to_anki_png(fen: str) -> str:
    def generate_svg_from_fen(fen):
        board = chess.Board(fen)
        svg_board = chess.svg.board(board=board)
        return svg_board

    def png_from_svg(svg):
        png_output = BytesIO()
        cairosvg.svg2png(bytestring=svg, write_to=png_output)
        return png_output.getvalue()

    board_svg = generate_svg_from_fen(fen)
    board_png = png_from_svg(board_svg)
    return base64.b64encode(board_png).decode("utf-8")

