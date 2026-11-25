import xml.etree.ElementTree as et
from urllib.request import urlopen


NAMESPACE = {"m": "http://maven.apache.org/POM/4.0.0"}
TIMEOUT = 15


def build_pom_url(repository, package, version):
    """Формирует URL POM-файла пакета."""
    group_id, artifact_id = package.split(":")
    group_path = group_id.replace(".", "/")
    repository = repository.rstrip("/")

    return (
        f"{repository}/{group_path}/{artifact_id}/"
        f"{version}/{artifact_id}-{version}.pom"
    )


def read_properties(root):
    """Считывает свойства POM-файла."""
    properties = {}

    for element in root.findall("m:properties/*", NAMESPACE):
        name = element.tag.split("}")[-1]
        properties[name] = element.text

    return properties


def resolve_version(version, properties):
    """Подставляет значение переменной версии."""
    if version.startswith("${") and version.endswith("}"):
        name = version[2:-1]
        return properties.get(name, version)

    return version


def parse_dependencies(pom):
    """Извлекает прямые зависимости из POM-файла."""
    root = et.fromstring(pom)
    properties = read_properties(root)
    dependencies = []

    for dependency in root.findall(
        "m:dependencies/m:dependency", NAMESPACE
    ):
        group_id = dependency.findtext("m:groupId", "", NAMESPACE)
        artifact_id = dependency.findtext("m:artifactId", "", NAMESPACE)
        version = dependency.findtext("m:version", "", NAMESPACE)
        scope = dependency.findtext("m:scope", "compile", NAMESPACE)

        version = resolve_version(version, properties)

        if not version:
            version = "не указана в POM"

        dependencies.append(
            (f"{group_id}:{artifact_id}", version, scope)
        )

    return dependencies


def get_dependencies(repository, package, version):
    """Получает прямые зависимости пакета из Maven."""
    url = build_pom_url(repository, package, version)

    with urlopen(url, timeout=TIMEOUT) as response:
        pom = response.read()

    return parse_dependencies(pom)
