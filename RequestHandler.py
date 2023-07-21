import chess
import requests

url_masters_database = "https://explorer.lichess.ovh/masters"
url_lichess_database = "https://explorer.lichess.ovh/lichess"


def make_request(number_of_lines: int, fen: str, played: str, masters) -> dict:
    def create_query_url(base_url: str, queries: list[str]) -> str:
        if len(queries) == 0:
            return base_url
        query_url = base_url + "?"
        for query in queries:
            if query != "":
                query_url = query_url + query + "&"
        query_url.removesuffix("&")
        return query_url

    url = url_masters_database if masters else url_lichess_database
    fen = "fen=" + fen
    moves = "moves=" + str(number_of_lines)
    played = "play=" + played
    url = create_query_url(url, [fen, moves, played])
    json = None
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for failed responses (4xx, 5xx status codes)
        json = response.json()
        # Process the 'data' dictionary as needed
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
    except ValueError as e:
        print("Error parsing JSON response:", e)
    return json


def get_most_common_moves(json: dict) -> list[str]:
    moves = []
    if json is not None and json['moves'] is not None:
        for move in json['moves']:
            moves.append(move['uci'])
    return moves


def get_opening_name(json: dict) -> str:
    if json['opening'] is not None and json['opening']['name'] is not None:
        return json['opening']['name']
    return ""


def played_string_from_list_of_moves(played: list[str]) -> str:
    """

    :param played: List of moves in UCI format
    :return: comma seperated list of moves
    """
    play = ''
    for move in played:
        play = play + move + ","
    play = play.removesuffix(",")
    return play


def get_fen_from_moves(moves: list[str]) -> str:
    board = chess.Board()
    for move in moves:
        board.push_uci(move)
    return board.fen()


def retrieve_position_information(number_of_lines: int, played: list[str] = None,
                                  masters=True):
    """

    :param played: Comma seperated moves played so far in UCI notation
    :param number_of_lines: number of top lines played to be returned
    :param masters: Whether to query the masters database or all games
    :return: PositionInformation object containing necessary information from database
    """

    class PositionInformation:
        fen: str
        common_moves: list[str]
        name: str

        def __init__(self, position_fen, position_common_moves, name):
            self.fen = position_fen
            self.common_moves = position_common_moves
            self.name = name

    if played is None:
        played = []

    played_string = played_string_from_list_of_moves(played)
    json = make_request(number_of_lines=number_of_lines, fen=chess.STARTING_FEN, played=played_string, masters=masters)
    fen = get_fen_from_moves(played)
    moves = get_most_common_moves(json)
    name = get_opening_name(json)
    info = PositionInformation(fen, moves, name)
    return info
