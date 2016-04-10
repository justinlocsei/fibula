from boto.exception import S3ResponseError

from fibula.actions.base import BaseAction
from fibula.data import load_data


class Backups(BaseAction):
    """A collection of actions for manipulating S3 backups."""

    log_prefix = 'backups'

    def configure(self):
        """Configure S3 buckets used for storing backups."""
        s3 = self.s3.connection
        buckets  = load_data('backups')['s3_buckets']

        for bucket in buckets:
            ui = self.ui.group(bucket['name'])

            try:
                remote_bucket = s3.get_bucket(bucket['name'])
            except S3ResponseError:
                remote_bucket = s3.create_bucket(bucket['name'])
                ui.create('Created S3 bucket')
            else:
                ui.skip('Bucket present')
