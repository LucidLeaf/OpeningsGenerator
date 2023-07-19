import requests

url_masters_database = "https://explorer.lichess.ovh/masters"
url_lichess_database = "https://explorer.lichess.ovh/lichess"


def make_request(fen: str, num_moves: int, masters=True):
    data = None
    url = url_masters_database if masters else url_lichess_database
    fen = "fen=" + fen
    moves = "moves=" + str(num_moves)
    url = url + "?" + fen + "&" + moves + "&" + "topGames=0"
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

if __name__ == "__main__":
    print(make_request("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", num_moves=3))