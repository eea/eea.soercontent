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
        title = root.Title()
        # split title on em dashes if matched
        # else returns original string wrapped
        # within a list
        splitted_title = title.split("\xe2\x80\x94")
        stripped_title = splitted_title[0].strip()
        return stripped_title

    def __call__(self, **kwargs):
        return self.template()
