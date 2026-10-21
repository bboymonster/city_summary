import time
import requests
from requests.exceptions import ConnectionError, Timeout
from clients.exceptions import ServiceUnavailableError

RETRY_STATUS_CODES = {500, 502, 503, 504}


def get_with_retry(
    url: str,
    params: dict = None,
    timeout: float = 10.0,
    max_retries: int = 2,
) -> requests.Response:
    """
    Выполняет GET-запрос с поддержкой timeout и повторов при сбоях сети/5xx/429.
    Возвращает объект requests.Response.
    При исчерпании попыток выбрасывает ServiceUnavailableError.
    """
    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            response = requests.get(url, params=params, timeout=timeout)

            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                try:
                    delay = float(retry_after) if retry_after else 1.0
                except (ValueError, TypeError):
                    delay = 1.0
                time.sleep(delay)
                continue

            if response.status_code in RETRY_STATUS_CODES:
                time.sleep(0.5 * (2 ** attempt))
                continue

            return response

        except (ConnectionError, Timeout) as exc:
            last_exception = exc
            if attempt < max_retries:
                time.sleep(0.5 * (2 ** attempt))
            continue

    raise ServiceUnavailableError(
        f"Сервис недоступен после {max_retries + 1} попыток: {url}"
    ) from last_exception