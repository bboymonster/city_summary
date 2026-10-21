from clients.exceptions import EntityNotFoundError
from clients.http import get_with_retry

WMO_CODES = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "fog",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    71: "slight snow",
    73: "moderate snow",
    75: "heavy snow",
    80: "rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    85: "snow showers",
    86: "heavy snow showers",
    95: "thunderstorm",
}


def get_weather(city: str) -> dict:
    """Получает текущую погоду для указанного города."""
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_resp = get_with_retry(
        geo_url,
        params={"name": city, "count": 1, "language": "en", "format": "json"},
    )

    if geo_resp.status_code != 200:
        raise EntityNotFoundError(f"Город '{city}' не найден")

    try:
        geo_data = geo_resp.json()
    except ValueError:
        raise EntityNotFoundError(f"Город '{city}' не найден")

    results = geo_data.get("results")
    if not results:
        raise EntityNotFoundError(f"Город '{city}' не найден")

    lat = results[0].get("latitude")
    lon = results[0].get("longitude")
    if lat is None or lon is None:
        raise EntityNotFoundError(f"Город '{city}' не найден")

    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_resp = get_with_retry(
        weather_url,
        params={"latitude": lat, "longitude": lon, "current_weather": "true"},
    )

    if weather_resp.status_code != 200:
        raise EntityNotFoundError(f"Не удалось получить погоду для '{city}'")

    try:
        weather_data = weather_resp.json()
    except ValueError:
        raise EntityNotFoundError(f"Не удалось получить погоду для '{city}'")

    current = weather_data.get("current_weather")
    if not current or "temperature" not in current:
        raise EntityNotFoundError(f"Не удалось получить погоду для '{city}'")

    code = current.get("weathercode", 0)
    description = WMO_CODES.get(code, "clear sky")

    return {
        "temp_c": float(current["temperature"]),
        "description": description,
    }