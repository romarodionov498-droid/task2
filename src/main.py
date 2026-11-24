import csv
import re
from pathlib import Path
from urllib.parse import urlparse
from xml.etree.ElementTree import ParseError

from src.graph import (
    build_graph,
    get_maven_dependencies,
    get_test_dependencies,
    read_test_repository,
)
from src.loading import get_loading_order


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
CSV_COLUMNS = 2


def read_config(path):
    """Считывает параметры из CSV-файла."""
    config = {}

    with open(path, encoding="utf-8", newline="") as file:
        for row in csv.reader(file):
            if len(row) != CSV_COLUMNS:
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


def create_graph(config):
    """Строит граф для выбранного режима работы."""
    package = config["package"]
    max_depth = int(config["max_depth"])

    if config["test_mode"] == "true":
        repository = read_test_repository(config["repository"])

        def get_children(node):
            """Получает зависимости тестового пакета."""
            return get_test_dependencies(repository, node)

    else:
        repository = config["repository"]
        package = f"{package}:{config['version']}"

        def get_children(node):
            """Получает зависимости Maven-пакета."""
            return get_maven_dependencies(repository, node)

    return build_graph(package, get_children, max_depth)


def main():
    """Определяет и выводит порядок загрузки зависимостей."""
    try:
        config = read_config(CONFIG_PATH)
        validate_config(config)

        graph = create_graph(config)
        package = next(iter(graph))
        order = get_loading_order(graph, package)

        print("Порядок загрузки зависимостей:")

        for number, dependency in enumerate(order, start=1):
            print(f"{number}. {dependency}")

    except (OSError, ValueError, ParseError, RecursionError) as error:
        print(f"Ошибка: {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())