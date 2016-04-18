#!/usr/bin/env python

import string
import random
import re


characters = ''.join([string.ascii_letters, string.digits, string.punctuation])
sanitized = re.sub(r'[\'"\\]', '', characters)

secret_key = ''.join([random.SystemRandom().choice(sanitized) for i in range(50)])
print secret_key
