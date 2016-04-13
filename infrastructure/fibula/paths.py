import os


INFRASTRUCTURE_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))
ANSIBLE_DIR = os.path.abspath(os.path.join(INFRASTRUCTURE_DIR, '..', 'ansible'))
DATA_DIR = os.path.join(INFRASTRUCTURE_DIR, 'data')
