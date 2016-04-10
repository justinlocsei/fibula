import os

import boto


class API:
    """An interface to the S3 API via boto."""

    def __init__(self):
        self._connection = None

    @property
    def connection(self):
        """A connection to S3

        Returns:
            boto.s3.connection.S3Connection
        """
        if not self._connection:
            self._connection = boto.connect_s3(
                os.environ['CYB_AWS_ACCESS_KEY_ID'],
                os.environ['CYB_AWS_SECRET_ACCESS_KEY']
            )

        return self._connection
