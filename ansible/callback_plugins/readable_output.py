from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.callback import CallbackBase
try:
    import simplejson as json
except ImportError:
    import json


LINE_BREAK_WIDTH = 75
FORMAT_FIELDS = [
  'cmd',
  'command',
  'delta',
  'end',
  'msg',
  'reason',
  'results',
  'start',
  'stderr',
  'stdout'
]


class CallbackModule(CallbackBase):
    """A callback that produces human-readable output.

    Inspired by: https://gist.github.com/dmsimard/cd706de198c85a8255f6
    """

    def runner_on_failed(self, host, res, ignore_errors=False):
        self._handle_result(res)

    def runner_on_ok(self, host, res):
        self._handle_result(res)

    def runner_on_unreachable(self, host, res):
        self._handle_result(res)

    def runner_on_async_poll(self, host, res, jid, clock):
        self._handle_result(res)

    def runner_on_async_ok(self, host, res, jid):
        self._handle_result(res)

    def runner_on_async_failed(self, host, res, jid):
        self._handle_result(res)

    def _handle_result(self, result):
        """Format any output that is part of a task's result."""
        if type(result) != dict:
            return

        break_shown = False
        for field in FORMAT_FIELDS:
            if field in result.keys() and result[field]:
                if not break_shown:
                  break_shown = True
                  print()
                output = self._format_output(result[field])
                print('{0}: {1}'.format(field, output.replace('\\n','\n')))

    def _format_output(self, output):
        """Format output to be human-readable.

        Args:
            output (str): The output of a command

        Returns:
            str: The human-readable output
        """

        # Transform unicode output to ASCII
        if type(output) == unicode:
            output = output.encode('ascii', 'replace')

        # Return pretty-printed JSON for dict results
        if type(output) == dict:
            return json.dumps(output, indent=2)

        # Show pretty-printed JSON for lists of potentially nested dicts
        if type(output) == list and type(output[0]) == dict:
            real_output = list()
            for index, item in enumerate(output):
                copy = item
                if type(item) == dict:
                    for field in FORMAT_FIELDS:
                        if field in item.keys():
                            copy[field] = self._format_output(item[field])
                real_output.append(copy)
            return json.dumps(output, indent=2)

        # Convert strings with newlines into an array of lines
        if type(output) == list and type(output[0]) != dict:
            real_output = list()
            for item in output:
                for string in item.split("\n"):
                    real_output.append(string)

            # Break long lines at an arbitrary character width
            if len(''.join(real_output)) > LINE_BREAK_WIDTH:
                return '\n' + '\n'.join(real_output)
            else:
                return ' '.join(real_output)

        # Return strings without modifications
        return output
