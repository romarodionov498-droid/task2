import json

from src.maven import get_dependencies


def read_test_repository(path):
    """Считывает описание тестового репозитория."""
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def get_test_dependencies(repository, package):
    """Возвращает зависимости тестового пакета."""
    if package not in repository:
        raise ValueError(f"Пакет не найден: {package}")

    return repository[package]


def get_maven_dependencies(repository, node):
    """Возвращает зависимости Maven для построения графа."""
    package, version = node.rsplit(":", 1)
    dependencies = get_dependencies(repository, package, version)
    result = []

    for name, version, scope in dependencies:
        if scope not in ("compile", "runtime"):
            continue

        if version == "не указана в POM" or "${" in version:
            raise ValueError(f"Не определена версия пакета: {name}")

        result.append(f"{name}:{version}")

    return result


def bfs_recursive(level, graph, get_children, depth, max_depth):
    """Рекурсивно обходит граф по уровням."""
    if not level or depth >= max_depth:
        return

    next_level = []

    for package in level:
        dependencies = get_children(package)
        graph[package] = dependencies

        for dependency in dependencies:
            if dependency not in graph:
                graph[dependency] = []
                next_level.append(dependency)

    bfs_recursive(
        next_level, graph, get_children, depth + 1, max_depth
    )


def build_graph(package, get_children, max_depth):
    """Строит граф зависимостей заданного пакета."""
    graph = {package: []}

    bfs_recursive(
        [package], graph, get_children, 0, max_depth
    )

    return graph