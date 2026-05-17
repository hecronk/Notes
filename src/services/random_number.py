import requests


def get_random_numbers(count):
    try:
        if not isinstance(count, int):
            raise ValueError("count must be int")

        url = f"http://www.randomnumberapi.com/api/v1.0/random?min=100&max=1000&count={count}"

        response = requests.get(url, timeout=5)
        response.raise_for_status()

        return {
            "data": response.json()[0],
            "errors": dict()
        }
    except Exception as e:
        return {
            "data": list(),
            "errors": [str(e),]
        }
