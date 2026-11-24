def visit(package, graph, visited, active, order):
    """Обрабатывает пакет и его зависимости."""
    if package in active:
        raise ValueError("Обнаружена циклическая зависимость")

    if package in visited:
        return

    active.add(package)

    for dependency in graph[package]:
        visit(dependency, graph, visited, active, order)

    active.remove(package)
    visited.add(package)
    order.append(package)


def get_loading_order(graph, package):
    """Определяет порядок загрузки зависимостей."""
    visited = set()
    active = set()
    order = []

    visit(package, graph, visited, active, order)

    return order