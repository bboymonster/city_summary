def apply_weather_rules(weather_data: dict) -> dict:
    """Применяет правила к данным погоды."""
    result = dict(weather_data)
    result["warm_clothes"] = result.get("temp_c", 0) < 0
    return result


def apply_rate_rules(rate: float, currency: str) -> dict:
    """Применяет правила к данным курса валюты."""
    return {
        "currency": currency.upper().strip(),
        "rate_to_rub": rate,
        "expensive": rate > 100,
    }