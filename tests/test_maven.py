import unittest

from src.maven import build_pom_url, parse_dependencies


class TestMaven(unittest.TestCase):
    """Проверяет получение данных о зависимостях."""

    def test_build_pom_url(self):
        """Проверяет формирование URL."""
        url = build_pom_url(
            "https://repo.maven.apache.org/maven2",
            "org.apache.commons:commons-text",
            "1.12.0",
        )

        expected = (
            "https://repo.maven.apache.org/maven2/"
            "org/apache/commons/commons-text/"
            "1.12.0/commons-text-1.12.0.pom"
        )

        self.assertEqual(url, expected)

    def test_direct_dependency(self):
        """Проверяет извлечение прямой зависимости."""
        pom = """
        <project xmlns="http://maven.apache.org/POM/4.0.0">
            <dependencies>
                <dependency>
                    <groupId>org.example</groupId>
                    <artifactId>library</artifactId>
                    <version>1.0</version>
                </dependency>
            </dependencies>
        </project>
        """

        expected = [("org.example:library", "1.0", "compile")]
        self.assertEqual(parse_dependencies(pom), expected)

    def test_no_dependencies(self):
        """Проверяет пакет без зависимостей."""
        pom = """
        <project xmlns="http://maven.apache.org/POM/4.0.0">
        </project>
        """

        self.assertEqual(parse_dependencies(pom), [])

    def test_version_property(self):
        """Проверяет подстановку переменной версии."""
        pom = """
        <project xmlns="http://maven.apache.org/POM/4.0.0">
            <properties>
                <library.version>2.0</library.version>
            </properties>
            <dependencies>
                <dependency>
                    <groupId>org.example</groupId>
                    <artifactId>library</artifactId>
                    <version>${library.version}</version>
                </dependency>
            </dependencies>
        </project>
        """

        expected = [("org.example:library", "2.0", "compile")]
        self.assertEqual(parse_dependencies(pom), expected)