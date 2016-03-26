from fibula.actions.base import BaseAction
from fibula.data import load_data


class Images(BaseAction):
    """A collection of actions for manipulating Digital Ocean images."""

    log_prefix = 'images'

    def list(self):
        """List all available images."""
        images = sorted(
            self.do.get_distro_images(),
            key=lambda d: '%s %s' % (d.distribution, d.name)
        )

        for image in images:
            ui = self.ui.group(str(image.id))
            ui.info('%s %s (%s)' % (image.distribution, image.name, image.slug))
