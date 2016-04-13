import json
import urllib

from boto.exception import BotoServerError, S3ResponseError
from boto.s3.lifecycle import Expiration, Lifecycle, Rule

from fibula.actions.base import BaseAction
from fibula.data import load_data


class Backups(BaseAction):
    """A collection of actions for manipulating S3 backups."""

    log_prefix = 'backups'

    def configure(self):
        """Configure S3 buckets used for storing backups."""
        s3 = self.s3.connection
        iam = self.iam.connection

        backups = load_data('backups')
        lifecycle_source = backups['lifecycle']

        for bucket in backups['s3_buckets']:
            ui = self.ui.group(bucket['name'])

            try:
                remote_bucket = s3.get_bucket(bucket['name'])
            except S3ResponseError:
                remote_bucket = s3.create_bucket(bucket['name'])
                ui.create('Created S3 bucket')
            else:
                ui.skip('Bucket present')

            try:
                lifecycle = remote_bucket.get_lifecycle_config()
            except S3ResponseError:
                ui.create('Created lifecycle policy')
                lifecycle = self._create_lifecycle_config(lifecycle_source)
                remote_bucket.configure_lifecycle(lifecycle)
            else:
                if self._lifecycle_differs(lifecycle, lifecycle_source):
                    ui.update('Synced lifecycle policy')
                    new_lifecycle = self._create_lifecycle_config(lifecycle_source)
                    remote_bucket.configure_lifecycle(new_lifecycle)
                else:
                    ui.skip('Lifecycle policy valid')

            policy_name = 's3-admin-%s' % bucket['name']
            base_policy = self._create_bucket_policy(bucket['name'])
            formatted_policy = self._format_policy(base_policy)

            try:
                policy = iam.get_user_policy(bucket['user'], policy_name)
            except BotoServerError as e:
                if e.status == 404:
                    ui.create('Created an access policy for the bucket user')
                    iam.put_user_policy(bucket['user'], policy_name, formatted_policy)
                else:
                    raise e
            else:
                raw_text = policy['get_user_policy_response']['get_user_policy_result']['policy_document']
                policy_text = json.loads(urllib.unquote(raw_text))
                if self._format_policy(policy_text) == formatted_policy:
                    ui.skip('User access policy valid')
                else:
                    ui.update('Synced user policy with the definition')
                    iam.put_user_policy(bucket['user'], policy_name, formatted_policy)

    def _create_lifecycle_config(self, source):
        """Create a lifecycle configuration for an S3 bucket.

        Args:
            source (dict): The definition for the lifecycle

        Returns:
            boto.s3.lifecycle.Lifecycle
        """
        lifecycle = Lifecycle()
        lifecycle.append(Rule(
            id=source['name'],
            status='Enabled',
            expiration=Expiration(days=source['expiration'])
        ))

        return lifecycle

    def _lifecycle_differs(self, actual, definition):
        """Determine whether an actual lifecycle differs from the definition.

        Args:
            actual (boto.s3.lifecycle.Lifecycle): An actual bucket lifecycle
            definition (dict): The lifecycle's definition

        Returns:
            bool: Whether the lifecycle differs from its definition
        """
        rule = actual[0]

        return any([
            rule.id != definition['name'],
            rule.status != 'Enabled',
            getattr(rule.expiration, 'days', 0) != definition['expiration'],
            rule.transition is not None
        ])

    def _create_bucket_policy(self, bucket_name):
        """Create an IAM user policy that grants access to a named bucket.

        Args:
            bucket_name (str): The name of an S3 bucket

        Returns:
            dict: An IAM user policy
        """
        return {
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "s3:ListAllMyBuckets",
                    "Resource": "arn:aws:s3:::*"
                },
                {
                    "Effect": "Allow",
                    "Action": "s3:*",
                    "Resource": [
                        "arn:aws:s3:::%s" % bucket_name,
                        "arn:aws:s3:::%s/*" % bucket_name
                    ]
                }
            ]
        }

    def _format_policy(self, policy):
        """Format a policy as a JSON string.

        Args:
            policy (dict): An IAM user policy

        Returns:
            str: The JSON version of the policy
        """
        return json.dumps(policy, indent=4)
