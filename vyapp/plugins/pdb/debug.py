"""

"""
from untwisted.network import core, cmap, READ, Device
from untwisted.tkinter import extern
from subprocess import Popen, PIPE, STDOUT
from untwisted.utils.iofd import *
from untwisted.utils.shrug import *
from vyapp.plugins.pdb import event
from vyapp.tools.misc import set_status_msg
from vyapp.tools.misc import get_opened_files, set_line, get_all_areavi_instances
from vyapp.ask import Ask

import sys
from os import environ, setsid, killpg
import shlex

class Pdb(object):
    def __call__(self, area, setup={'background':'blue', 'foreground':'yellow'}):

        INSTALL = ((3, '<Key-p>', lambda event: self.stdin.dump('print %s' % event.widget.tag_get_ranges('sel', sep='\r\n'))), 
                   (3, '<Key-1>', lambda event: self.start_debug(event.widget)), 
                   (3, '<Key-c>', lambda event: self.stdin.dump('continue\r\n')), 
                   (3, '<Key-e>', lambda event: self.stdin.dump('!%s' % event.widget.tag_get_ranges('sel', sep='\r\n'))), 
                   (3, '<Key-w>', lambda event: self.stdin.dump('where\r\n')), 
                   (3, '<Key-a>', lambda event: self.stdin.dump('args\r\n')), 
                   (3, '<Key-s>', lambda event: self.stdin.dump('step\r\n')), 
                   (3, '<Control-C>', lambda event: self.stdin.dump('clear\r\nyes\r\n')), 
                   (3, '<Control-c>', lambda event: self.stdin.dump('clear %s\r\n' % self.map_line[(event.widget.filename, str(event.widget.indref('insert')[0]))])),
                   (3, '<Key-B>', lambda event: self.stdin.dump('tbreak %s:%s\r\n' % (event.widget.filename, event.widget.indref('insert')[0]))),
                   (3, '<Key-b>', lambda event: self.stdin.dump('break %s:%s\r\n' % (event.widget.filename, event.widget.indref('insert')[0]))))

        area.install(*INSTALL)
        self.setup = setup

    def __init__(self):
        self.child = None
        self.map_index  = dict()
        self.map_line   = dict()

    def start_debug(self, area):
        try:
            self.child.kill()
        except Exception:
            pass

        # When the process is restarted we need to remove all breakpoint tags.
        self.clear_breakpoint_map()

        ask         = Ask(area, 'Arguments')
        ARGS        = 'python -u -m pdb %s %s' % (area.filename, ask.data)
        ARGS        = shlex.split(ARGS)

        self.child  = Popen(ARGS, shell=0, stdout=PIPE, stdin=PIPE, preexec_fn=setsid, 
                            stderr=STDOUT,  env=environ)
    
        self.stdout = Device(self.child.stdout)
        self.stdin  = Device(self.child.stdin)
    
        Stdout(self.stdout)
        Shrug(self.stdout, delim='\n')
        Stdin(self.stdin)
        event.install(self.stdout)

        xmap(self.stdout, LOAD, lambda con, data: sys.stdout.write(data))

        xmap(self.stdout, 'LINE', self.handle_line)
        xmap(self.stdout, 'DELETED_BREAKPOINT', self.handle_deleted_breakpoint)
        xmap(self.stdout, 'BREAKPOINT', self.handle_breakpoint)

        xmap(self.stdin, CLOSE, lambda dev, err: lose(dev))
        xmap(self.stdout, CLOSE, lambda dev, err: lose(dev))

        set_status_msg('Debug process started !')
            
    def clear_breakpoint_map(self):
        """

        """

        for index, (filename, line) in self.map_index.iteritems():
            try:
                area = get_opened_files()[filename]
            except KeyError:
                pass
            else:
                NAME = '_breakpoint_%s' % index
                area.tag_delete(NAME)        
    
        self.map_index.clear()
        self.map_line.clear()

    def handle_line(self, device, filename, line, args):
    
        """
    
        """
        try:
            area = get_opened_files()[filename]
        except  KeyError:
            pass
        else:
            set_line(area, line)
    
    def handle_deleted_breakpoint(self, device, index):
        """
        When a break point is removed.
        """

        filename, line = self.map_index[index]
        NAME           = '_breakpoint_%s' % index
        area           = None

        try:
            area = get_opened_files()[filename]
        except KeyError:
            return

        area.tag_delete(NAME)

    def handle_breakpoint(self, device, index, filename, line):
        """
        When a break point is added.
        """

        self.map_index[index]           = (filename, line)
        self.map_line[(filename, line)] = index
        map                             = get_opened_files()

        area = map[filename]
        
        NAME = '_breakpoint_%s' % index
        area.tag_add(NAME, '%s.0 linestart' % line, 
                     '%s.0 lineend' % line)
    
        area.tag_config(NAME, **self.setup)

    def dump_sigint(self, area):
        killpg(child.pid, 2)


pdb     = Pdb()
install = pdb













