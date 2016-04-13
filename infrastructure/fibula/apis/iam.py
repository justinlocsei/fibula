import os

import boto


class API:
    """An interface to the AWS IAM API via boto."""

    def __init__(self):
        self._connection = None

    @property
    def connection(self):
        """A connection to IAM

        Returns:
            boto.iam.connection.IAMConnection
        """
        if not self._connection:
            self._connection = boto.connect_iam(
                os.environ['CYB_AWS_ACCESS_KEY_ID'],
                os.environ['CYB_AWS_SECRET_ACCESS_KEY']
            )

        return self._connection
