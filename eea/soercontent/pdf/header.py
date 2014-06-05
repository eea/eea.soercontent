""" PDF Views
"""
from eea.pdf.utils import getApplicationRoot
from Products.Five.browser import BrowserView

class Header(BrowserView):
    """ PDF Header
    """
    def title(self):
        """ Root title
        """
        root = getApplicationRoot(self.context)
        return root.Title()
