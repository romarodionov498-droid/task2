import unittest
from pathlib import Path

from src.graph import (
    build_graph,
    get_test_dependencies,
    read_test_repository,
)
from src.loading import get_loading_order


TEST_PATH = (
    Path(__file__).resolve().parents[1] / "test_repository.json"
)


class TestLoading(unittest.TestCase):
    """Проверяет порядок загрузки зависимостей."""

    def setUp(self):
        """Загружает тестовый репозиторий."""
        self.repository = read_test_repository(TEST_PATH)

    def get_children(self, package):
        """Получает зависимости тестового пакета."""
        return get_test_dependencies(self.repository, package)

    def test_loading_order(self):
        """Проверяет порядок и общую зависимость."""
        graph = build_graph("F", self.get_children, 3)
        order = get_loading_order(graph, "F")

        self.assertEqual(order, ["I", "G", "H", "F"])

    def test_cycle(self):
        """Проверяет обработку циклической зависимости."""
        graph = build_graph("A", self.get_children, 3)

        with self.assertRaises(ValueError):
            get_loading_order(graph, "A")

    def test_no_dependencies(self):
        """Проверяет пакет без зависимостей."""
        graph = build_graph("I", self.get_children, 3)
        order = get_loading_order(graph, "I")

        self.assertEqual(order, ["I"])

    def test_max_depth(self):
        """Проверяет ограничение глубины."""
        graph = build_graph("F", self.get_children, 1)
        order = get_loading_order(graph, "F")

        self.assertEqual(order, ["G", "H", "F"])