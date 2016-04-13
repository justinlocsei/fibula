import subprocess

from fibula.actions.base import BaseAction
from fibula.paths import ANSIBLE_DIR


ENVIRONMENTS = ('development', 'staging')


class Deploy(BaseAction):
    """A collection of actions for deploying application code."""

    log_prefix = 'deploy'

    def bootstrap(self, environment, inventory, user):
        """Bootstrap hosts for deployment.

        Args:
            environment (str): The name of a remote environment
            inventory (str): The name of an inventory file
            user (str): The SSH user for the connection
        """
        self._run_playbook('provision.yml', environment, inventory, user=user)

    def deploy(self, environment, inventory):
        """Deploy code to a given environment.

        Args:
            environment (str): The name of an environment
            inventory (str): The name of an inventory file
        """
        self._run_playbook('deploy.yml', environment, inventory)

    def roll_back(self, environment, inventory):
        """Roll back deploy code for a given environment.

        Args:
            environment (str): The name of an environment
            inventory (str): The name of an inventory file
        """
        self._run_playbook('rollback.yml', environment, inventory)

    def _run_playbook(self, playbook, limit, inventory, user=None):
        """Run an Ansible playbook.

        Args:
            playbook (str): The name of an ansible playbook file
            limit (str): The limit option to use
            inventory (str): The name of an inventory file

        Keyword Args:
            user (str): The SSH user to use when connecting
        """
        ansible_args = [
            'ansible-playbook', 'playbooks/%s' % playbook,
            '--limit', limit,
            '--inventory-file', 'inventories/%s' % inventory,
            '-v'
        ]

        if user:
            ansible_args.append('--user')
            ansible_args.append(user)

        playbook = subprocess.Popen(ansible_args, cwd=ANSIBLE_DIR)
        playbook.wait()
