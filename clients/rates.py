from clients.exceptions import EntityNotFoundError
from clients.http import get_with_retry


def get_rate(currency: str = "USD") -> float:
    """Получает курс валюты к рублю через Frankfurter API."""
    code = currency.upper().strip()
    url = f"https://api.frankfurter.dev/v2/rate/{code}/RUB"
    response = get_with_retry(url)

    if response.status_code != 200:
        raise EntityNotFoundError(f"Код валюты '{currency}' не найден")

    try:
        data = response.json()
    except ValueError:
        raise EntityNotFoundError(f"Код валюты '{currency}' не найден")

    if "rate" in data:
        return float(data["rate"])
    if "rates" in data and "RUB" in data["rates"]:
        return float(data["rates"]["RUB"])

    raise EntityNotFoundError(f"Код валюты '{currency}' не найден")