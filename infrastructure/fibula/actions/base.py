from fibula.apis.do import DO
from fibula.communicator import Communicator


class BaseAction:
    """An abstract base action for managing infrastructure."""

    log_prefix = None

    def __init__(self):
        """Create a new action."""
        self.ui = Communicator(label=self.log_prefix)

        self.do = DO()
