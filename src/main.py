import csv
import re
from pathlib import Path
from urllib.parse import urlparse
from xml.etree.ElementTree import ParseError

from src.maven import get_dependencies


CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.csv"

REQUIRED_KEYS = (
    "package",
    "repository",
    "test_mode",
    "version",
    "output_file",
    "max_depth",
)

MIN_DEPTH = 0


def read_config(path):
    """Считывает параметры из CSV-файла."""
    config = {}

    with open(path, encoding="utf-8", newline="") as file:
        for row in csv.reader(file):
            if len(row) != 2:
                raise ValueError("Некорректный формат CSV")

            key, value = row

            if key in config:
                raise ValueError(f"Повтор параметра: {key}")

            config[key] = value.strip()

    return config


def validate_repository(repository, test_mode):
    """Проверяет адрес репозитория или путь к файлу."""
    if test_mode == "true":
        if not Path(repository).is_file():
            raise ValueError("Тестовый файл не найден")
    else:
        url = urlparse(repository)
        if url.scheme not in ("http", "https") or not url.hostname:
            raise ValueError("Некорректный URL репозитория")


def validate_config(config):
    """Проверяет корректность параметров конфигурации."""
    for key in REQUIRED_KEYS:
        if not config.get(key):
            raise ValueError(f"Отсутствует параметр: {key}")

    if config["test_mode"] not in ("true", "false"):
        raise ValueError("test_mode должен быть true или false")

    pattern = r"[\w.-]+:[\w.-]+"
    if config["test_mode"] == "true":
        pattern = r"[A-Z]+"

    if not re.fullmatch(pattern, config["package"]):
        raise ValueError("Некорректное имя пакета")

    validate_repository(config["repository"], config["test_mode"])

    if not re.fullmatch(r"[\w.+-]+", config["version"]):
        raise ValueError("Некорректная версия пакета")

    if not re.fullmatch(r"[\w.-]+\.svg", config["output_file"]):
        raise ValueError("Некорректное имя SVG-файла")

    if not config["max_depth"].isdigit():
        raise ValueError(
            "Глубина должна быть целым неотрицательным числом"
        )

    if int(config["max_depth"]) < MIN_DEPTH:
        raise ValueError("Некорректная глубина")


def main():
    """Получает и выводит прямые зависимости пакета."""
    try:
        config = read_config(CONFIG_PATH)
        validate_config(config)

        dependencies = get_dependencies(
            config["repository"],
            config["package"],
            config["version"],
        )

        print(f"Пакет: {config['package']}")
        print(f"Версия: {config['version']}")
        print("Прямые зависимости:")

        for package, version, scope in dependencies:
            print(f"{package} — {version} ({scope})")

        if not dependencies:
            print("Зависимости отсутствуют")

    except (OSError, ValueError, ParseError) as error:
        print(f"Ошибка: {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())