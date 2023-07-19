from pprint import pprint

import requests

url_masters_database = "https://explorer.lichess.ovh/masters"
url_lichess_database = "https://explorer.lichess.ovh/lichess"
initial_game_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def make_request(fen: str, played: str, number_of_lines: int, masters=True) -> dict:
    """

    :param fen: FEN string of the position
    :param played: Comma seperated moves played so far in UCI notation
    :param number_of_lines: number of top lines played to be returned
    :param masters: Whether to query the masters database or all games
    :return: dictionary containing json response
    """

    def create_query_url(base_url: str, queries: [str]):
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
    played = "" if played == "" else "play=" + played
    url = create_query_url(url, [fen, moves, played])
    data = None
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for failed responses (4xx, 5xx status codes)
        data = response.json()
        # Process the 'data' dictionary as needed
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
    except ValueError as e:
        print("Error parsing JSON response:", e)
    return data


def get_most_common_moves(data: dict):
    moves = []
    for move in data['moves']:
        moves.append(move['uci'])
    return moves


def get_opening_name(data: dict):
    if data['opening'] != None and data['opening']['name'] != None:
        return data['opening']['name']
    return ""


if __name__ == "__main__":
    data = make_request(fen=initial_game_fen, played="", number_of_lines=4,
                        masters=True)
    pprint(data)
    print(get_opening_name(data))
    print("Most common responses:")
    pprint(get_most_common_moves(data))
