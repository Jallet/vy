"""
Overview
========

This plugin implements Key-Commands to scroll lines.

Key-Commands
============

Mode: NORMAL
Event: <Key-w> 
Description: Scroll one line up.


Mode: NORMAL
Event: <Key-s> 
Description: Scroll one line down.
"""

def install(area):
    area.install(('NORMAL', '<Key-w>', lambda event: event.widget.scroll_line_up()),
                 ('NORMAL', '<Key-s>', lambda event: event.widget.scroll_line_down()))





