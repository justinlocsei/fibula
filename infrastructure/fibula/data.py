import os
import yaml

from fibula.paths import DATA_DIR


def load_data(path):
    """Load a named YAML data file.

    Args:
        path (str): The path to the file, relative to the data directory

    Returns:
        dict: The parsed data file

    Raise:
        IOError: When the file cannot be loaded
    """
    if not path.endswith('.yml'):
        path = '%s.yml' % path
    fullpath = os.path.join(DATA_DIR, path)

    with open(fullpath) as file:
        return yaml.load(file)
