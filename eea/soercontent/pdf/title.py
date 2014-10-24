""" PDF View
"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.pdf.themes.page.cover import Cover
from eea.pdf.utils import getApplicationRoot

class Title(Cover):
    """ Custom PDF body
    """
    template = ViewPageTemplateFile('title.pt')

    @property
    def root(self):
        """ Navigation root
        """
        return getApplicationRoot(self.context)

    @property
    def parent(self):
        """ Parent
        """
        return self.context.getParentNode()
