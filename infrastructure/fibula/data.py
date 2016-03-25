import os
import yaml

INFRA_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))
DATA_DIR = os.path.join(INFRA_DIR, 'data')

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
