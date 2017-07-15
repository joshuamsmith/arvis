#!/usr/bin/python
import re

import connectwise


def process_message(message):
    search_obj = re.search(r'#(\d+)', message)
    if search_obj:
        # Lookup and return SR# details if found
        reply = connectwise.return_sr_summary(search_obj.group(1))
    else:
        reply = 'Error: unsure how to handle.'
    return reply

