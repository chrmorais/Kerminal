# encoding: utf-8

"""
"""

import curses
import sys
from npyscreen import TitleText, Textfield

from . import BaseContainer


#This is a re-implementation of the old WidgetContainer, starting from the
#ground-up as a BaseContainer subclass
class BoxContainer(BaseContainer):
    """
    A quite basic Container subclass, BoxContainer assumes all contained widgets
    will require one line, draws a box at its perimeter, and can optionally
    create a header and footer with one of (left, center, right) justification.
    """
    BORDER_MARGIN = 1
    #HEADER_JUSTIFY = 'left'  # left | center | right
    #FOOTER_JUSTIFY = 'left'  # left | center | right

    def __init__(self,
                 screen,
                 height=6,
                 width=26,
                 header=None,  # Header text
                 footer=None,  # Footer text
                 header_justify='left',  # str, one of (left, center, right)
                 footer_justify='left',  # str, one of (left, center, right)
                 header_color='LABEL',
                 footer_color='LABEL',
                 *args,
                 **kwargs):

        self.height = height
        self.width = width
        #self.header = header
        self.header = 'HEADER'
        #self.footer = footer
        self.footer = 'FOOTER'
        if header_justify in ('left', 'center', 'right'):
            self.header_justify = header_justify
        else:
            self.header_justify = 'left'
        if footer_justify in ('left', 'center', 'right'):
            self.footer_justify = footer_justify
        else:
            self.footer_justify = 'left'
        self.header_color = header_color
        self.footer_color = footer_color
        super(BoxContainer, self).__init__(screen,
                                           margin=self.__class__.BORDER_MARGIN,
                                           #height=6,
                                           #width=26,
                                           *args,
                                           **kwargs)
        self.make_header_and_footer()

    def make_header_and_footer(self):
        max_text_length = self.width - 3  # Two for the corners, one for blank
        justify_offsets = {'left': lambda x: 1,
                           'center': lambda x: (self.width - len(x)) // 2,
                           'right': lambda x: (self.width - len(x)) - 1}
        if self.header:
            if len(self.header) > (max_text_length):
                header_text = 'TOO LONG!'[:max_text_length]
            else:
                header_text = self.header
            x_offset = justify_offsets[self.header_justify](header_text)
            self.header_widget = Textfield(self.parent,
                                           relx=self.relx + x_offset,
                                           rely=self.rely,
                                           width=len(header_text) + 1,
                                           value=header_text,
                                           color=self.header_color)
        else:
            self.header_widget = None
        if self.footer:
            if len(self.footer) > (max_text_length):
                footer_text = 'TOO LONG!'[:max_text_length]
            else:
                footer_text = self.footer
            x_offset = justify_offsets[self.footer_justify](footer_text)
            self.footer_widget = Textfield(self.parent,
                                           relx=self.relx + x_offset,
                                           rely=self.rely + self.height - 1,
                                           width=len(footer_text) + 1,
                                           value=footer_text,
                                           color=self.footer_color)
        else:
            self.footer_widget = None

    def _resize(self):
        self.header_widget.relx = self.relx + 1
        self.footer_widget.relx = self.relx + 1
        self.header_widget.rely = self.rely
        self.footer_widget.rely = self.rely + self.height - 1
        for i, widget in enumerate(self.contained):
            widget.relx = self.relx + self.left_margin
            widget.width = self.width - (self.right_margin + self.left_margin)
            widget.rely = self.rely + self.top_margin + i
            widget.resize()

    def update(self, clear=True):
        super(BoxContainer, self).update(clear)

        for contained in self.contained:
            contained.update()

        #Time to draw the box; First the bars
        self.parent.curses_pad.hline(self.rely, self.relx + 1,
                                     curses.ACS_HLINE, self.width - 2)
        self.parent.curses_pad.hline(self.rely + self.height - 1, self.relx + 1,
                                     curses.ACS_HLINE, self.width - 2)
        self.parent.curses_pad.vline(self.rely + 1, self.relx,
                                     curses.ACS_VLINE, self.height - 2)
        self.parent.curses_pad.vline(self.rely + 1, self.relx + self.width - 1,
                                     curses.ACS_VLINE, self.height - 2)

        #Now the corners

        #Note! The following is a workaround to fix a bug in Python 3.4.0;
        #It should probably be addressed in npyscreen internally
        #For reference: http://bugs.python.org/issue21088
        #               https://hg.python.org/cpython/rev/c67a19e11a71
        #Should be fixed in release candidate 1 of 3.4.1, so I only check for
        #3.4.0
        #The bug causes the y,x arguments to be inverted to x,y

        def custom_addch(y, x, ch):
            if sys.version_info[:3] == (3, 4, 0):
                y, x = x, y
            self.parent.curses_pad.addch(y, x, ch)

        custom_addch(self.rely, self.relx,
                     curses.ACS_ULCORNER)
        custom_addch(self.rely, self.relx + self.width - 1,
                     curses.ACS_URCORNER)
        custom_addch(self.rely + self.height - 1, self.relx,
                     curses.ACS_LLCORNER)
        custom_addch(self.rely + self.height - 1, self.relx + self.width - 1,
                     curses.ACS_LRCORNER)

        if self.editing:
            if self.header_widget is not None:
                self.header_widget.show_bold = True
                self.header_widget.color = 'LABELBOLD'
            if self.footer_widget is not None:
                self.footer_widget.show_bold = True
                self.footer_widget.color = 'LABELBOLD'
        else:
            if self.header_widget is not None:
                self.header_widget.show_bold = False
                self.header_widget.color = self.header_color
            if self.footer_widget is not None:
                self.footer_widget.show_bold = False
                self.footer_widget.color = self.footer_color

        if self.header_widget is not None:
            self.header_widget.update()
        if self.footer_widget is not None:
            self.footer_widget.update()

    def calculate_area_needed(self):
        return self.height, self.width
        #return 0, 0