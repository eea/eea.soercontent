""" PDF Views
"""
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.pdf.utils import getApplicationRoot

class Header(BrowserView):
    """ PDF Header
    """
    template = ViewPageTemplateFile('header.pt')

    def title(self):
        """ Root title
        """
        root = getApplicationRoot(self.context)
        return root.Title()

    def __call__(self, **kwargs):
        return self.template()
