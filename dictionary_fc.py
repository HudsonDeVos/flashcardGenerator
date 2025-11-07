import requests

class Dictionary:
    @staticmethod
    def get_definition(word):
        api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            definition = data[0]["meanings"][0]["definitions"][0]["definition"]
            return definition
        except requests.exceptions.RequestException:
            return None
