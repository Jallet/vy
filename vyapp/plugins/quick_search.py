"""

"""

from vyapp.ask import Get
from vyapp.regutils import build_regex
from vyapp.app import root

class QuickSearch(object):
    def __init__(self, area, nocase=True, 
        setup={'background':'yellow', 'foreground':'black'}):

        """

        """
        self.area   = area
        self.nocase = nocase
        area.tag_configure('(SEARCH_MATCH)', **setup)

        area.install(
        ('NORMAL', '<Key-q>', self.start_backwards),
        ('NORMAL', '<Key-a>', self.start_forwards))



    def start_forwards(self, event):
        self.index     = self.area.index('insert')
        self.stopindex = 'end'
        self.backwards = False

        Get(self.area, events = {
        '<Alt-p>':self.search_down, 
        '<Alt-o>': self.search_up, 
        '<Control-j>': self.search_down,     
        '<Control-k>': self.search_up, 
        '<<Data>>': self.update, 
        '<BackSpace>': self.update,
        '<Return>':  self.done, 
        '<Escape>':  self.cancel})

    def start_backwards(self, event):
        self.index     = self.area.index('insert')
        self.backwards = True
        self.stopindex = '1.0'

        Get(self.area, events = {
        '<Alt-p>':self.search_down, 
        '<Alt-o>': self.search_up, 
        '<Control-j>': self.search_down,     
        '<Control-k>': self.search_up, 
        '<<Data>>': self.update, 
        '<BackSpace>': self.update,
        '<Return>':  self.done, 
        '<Escape>':  self.cancel})

    def cancel(self, wid):
        self.area.tag_remove('(SEARCH_MATCH)', '1.0', 'end')
        self.area.seecur(self.index)

        return True

    def done(self, wid):
        self.area.tag_remove('(SEARCH_MATCH)', '1.0', 'end')
        return True

    def update(self, wid):
        """

        """
        data    = wid.get()
        pattern = build_regex(data)
        root.status.set_msg('Pattern:%s' % pattern)
        self.area.ipick('(SEARCH_MATCH)', pattern,
        verbose=True, backwards=self.backwards, index=self.index, 
        nocase=self.nocase, stopindex=self.stopindex)

    def search_up(self, wid):
        """

        """
        data    = wid.get()
        pattern = build_regex(data)
        self.area.ipick('(SEARCH_MATCH)', pattern, index='insert', 
        nocase=self.nocase, stopindex='1.0', backwards=True)

    def search_down(self, wid):
        """

        """
        data    = wid.get()
        pattern = build_regex(data)
        self.area.ipick('(SEARCH_MATCH)', pattern, nocase=self.nocase, 
        stopindex='end', index='insert')


install = QuickSearch



