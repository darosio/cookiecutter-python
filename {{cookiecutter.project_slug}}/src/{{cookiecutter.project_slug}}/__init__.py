"""ClopHfit: Parse plate-reader and fit ClopHensor titrations."""
from pkg_resources import get_distribution  # type: ignore

__version__ = get_distribution('{{ cookiecutter.project_name }}').version
