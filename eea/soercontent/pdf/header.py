""" PDF Views
"""
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.soercontent.pdf.utils import split_root_title


class Header(BrowserView):
    """ PDF Header
    """
    template = ViewPageTemplateFile('header.pt')

    def title(self):
        """ Root title
        """
        return split_root_title(self.context, only_first_slice=True)

    def __call__(self, **kwargs):
        return self.template()
