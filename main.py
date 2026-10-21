import argparse
import sys
from clients.exceptions import EntityNotFoundError, ServiceUnavailableError
from processing.service import build_city_summary


def main():
    """Точка входа CLI."""
    parser = argparse.ArgumentParser(description="Сводка по городу")
    parser.add_argument("--city", required=True, help="Название города")
    parser.add_argument(
        "--currency", default="USD", help="ISO-код валюты (по умолчанию USD)"
    )
    args = parser.parse_args()

    try:
        summary = build_city_summary(city=args.city, currency=args.currency)
    except EntityNotFoundError as err:
        print(f"Ошибка: {err}", file=sys.stderr)
        sys.exit(3)
    except ServiceUnavailableError as err:
        print(f"Ошибка сервиса: {err}", file=sys.stderr)
        sys.exit(4)

    weather = summary["weather"]
    rates = summary["rates"]

    warm_clothes_text = "да" if weather["warm_clothes"] else "нет"
    expensive_text = "да" if rates["expensive"] else "нет"

    print(f"Город: {summary['city']}")
    print(f"Погода: {weather['temp_c']}°C, {weather['description']}")
    print(f"Тёплая одежда: {warm_clothes_text}")
    print(f"{rates['currency']}→RUB: {rates['rate_to_rub']}")
    print(f"Дорогой курс: {expensive_text}")
    sys.exit(0)


if __name__ == "__main__":
    main()