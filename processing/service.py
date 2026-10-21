from clients.rates import get_rate
from clients.weather import get_weather
from processing.preprocessing import apply_rate_rules, apply_weather_rules


def build_city_summary(city: str, currency: str = "USD") -> dict:
    """Собирает сводку по погоде и курсу валюты для города."""
    weather_raw = get_weather(city)
    rate_raw = get_rate(currency)

    return {
        "city": city,
        "weather": apply_weather_rules(weather_raw),
        "rates": apply_rate_rules(rate_raw, currency),
    }