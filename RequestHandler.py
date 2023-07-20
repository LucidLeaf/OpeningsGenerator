import requests

url_masters_database = "https://explorer.lichess.ovh/masters"
url_lichess_database = "https://explorer.lichess.ovh/lichess"
initial_game_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def make_request(number_of_lines: int, fen: str = initial_game_fen, played: list[str] = None, masters=True) -> dict:
    """

    :param fen: FEN string of the position
    :param played: Comma seperated moves played so far in UCI notation
    :param number_of_lines: number of top lines played to be returned
    :param masters: Whether to query the masters database or all games
    :return: dictionary containing json response
    """

    def create_query_url(base_url: str, queries: list[str]) -> str:
        if len(queries) == 0:
            return base_url
        query_url = base_url + "?"
        for query in queries:
            if query != "":
                query_url = query_url + query + "&"
        query_url.removesuffix("&")
        return query_url

    if played is None:
        played = []

    url = url_masters_database if masters else url_lichess_database
    fen = "fen=" + fen
    moves = "moves=" + str(number_of_lines)
    played = "play=" + played_string_from_list_of_moves(played)
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
