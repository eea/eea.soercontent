""" PDF View
"""
from eea.pdf.themes.classical.cover import Cover
from eea.pdf.utils import getApplicationRoot

class Title(Cover):
    """ Custom PDF body
    """
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
