import requests


class Dictionary: 
    word = input("Enter a word: ")
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        definition = data[0]["meanings"][0]["definitions"][0]["definition"]
        print(f"Definition of {word}: {definition}")
    except requests.exceptions.RequestException as e:
        print(f"not found {e}")
        print("Rerun the code and try retyping")