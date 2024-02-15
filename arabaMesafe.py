import requests


def get_driving_distance_car( origin, destination):
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "mode": "driving",
        "key": "your_apiKey",
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data["status"] == "OK":
        distance = data["routes"][0]["legs"][0]["distance"]["value"]
        return float(distance / 1000)
    else:
        return "Hata: Mesafe hesaplanamadı."


def calculate_distance_car( coordinates1, coordinates2):
    origin = f"{coordinates1[0]},{coordinates1[1]}"
    destination = f"{coordinates2[0]},{coordinates2[1]}"

    return get_driving_distance_car( origin, destination)
