import subprocess
import sys

from fibula.actions.base import BaseAction
from fibula.paths import ANSIBLE_DIR


ENVIRONMENTS = ('development', 'staging', 'production')


def confirm_deploy_action(action, hosts, inventory):
    """Prompt the user for confirmation of a deploy action.

    Args:
        action (str): The name of the action
        hosts (str): The hosts filter
        inventory (str): The inventory name

    Returns:
        bool: Whether the user confirmed the action or not
    """
    print 'Are you sure that you want to perform the following deploy?'
    print ''
    print '   ACTION = %s' % action
    print '    HOSTS = %s' % hosts
    print 'INVENTORY = %s' % inventory
    print ' '

    sys.stdout.write('Continue with this deploy? [y/n] ')
    choice = raw_input().lower()[0]
    return choice == 'y'


class Deploy(BaseAction):
    """A collection of actions for deploying application code."""

    log_prefix = 'deploy'

    def bootstrap(self, environment, inventory, user, tag, playbook):
        """Bootstrap hosts for deployment.

        Args:
            environment (str): The name of a remote environment
            inventory (str): The name of an inventory file
            user (str): The SSH user for the connection
            tag (str): The name of the tag to run
            playbook (str): The name of the playbook to run
        """
        self._run_playbook(playbook, environment, inventory, user=user, tag=tag)

    def deploy(self, environment, inventory, tag, playbook):
        """Deploy code to a given environment.

        Args:
            environment (str): The name of an environment
            inventory (str): The name of an inventory file
            tag (str): The name of the tag to run
            playbook (str): The name of the playbook to run
        """
        self._run_playbook(playbook, environment, inventory, tag=tag)

    def roll_back(self, environment, inventory):
        """Roll back deploy code for a given environment.

        Args:
            environment (str): The name of an environment
            inventory (str): The name of an inventory file
        """
        self._run_playbook('rollback.yml', environment, inventory)

    def _run_playbook(self, playbook, limit, inventory, tag=None, user=None):
        """Run an Ansible playbook.

        Args:
            playbook (str): The name of an ansible playbook file
            limit (str): The limit option to use
            inventory (str): The name of an inventory file

        Keyword Args:
            tag (str): The name of the tag to run
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

        if tag:
            ansible_args.append('--tags')
            ansible_args.append(tag)

        playbook = subprocess.Popen(ansible_args, cwd=ANSIBLE_DIR)
        playbook.wait()
