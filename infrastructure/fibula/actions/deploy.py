import subprocess

from fibula.actions.base import BaseAction
from fibula.paths import ANSIBLE_DIR


ENVIRONMENTS = ('development', 'staging')


class Deploy(BaseAction):
    """A collection of actions for deploying application code."""

    log_prefix = 'deploy'

    def deploy(self, environment, inventory, verbose=False):
        """Deploy code to a given environment.

        Args:
            environment (str): The name of an environment
            inventory (str): The name of an inventory file
            verbose (bool): Whether to enable verbose output
        """
        self._run_playbook('deploy.yml', environment, inventory, verbose)

    def roll_back(self, environment, inventory, verbose=False):
        """Roll back deploy code for a given environment.

        Args:
            environment (str): The name of an environment
            inventory (str): The name of an inventory file
            verbose (bool): Whether to enable verbose output
        """
        self._run_playbook('rollback.yml', environment, inventory, verbose)

    def _run_playbook(self, playbook, environment, inventory, verbose):
        """Run an Ansible playbook.

        Args:
            playbook (str): The name of an ansible playbook file
            environment (str): The name of an environment
            inventory (str): The name of an inventory file
            verbose (bool): Whether to enable verbose output
        """
        ansible_args = [
            'ansible-playbook', 'playbooks/%s' % playbook,
            '--limit', environment,
            '--inventory-file', 'inventories/%s' % inventory
        ]
        if verbose:
            ansible_args.append('-v')

        playbook = subprocess.Popen(ansible_args, cwd=ANSIBLE_DIR)
        playbook.wait()
