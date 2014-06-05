""" PDF Views
"""
from eea.pdf.utils import getApplicationRoot
from Products.Five.browser import BrowserView

class Footer(BrowserView):
    """ PDF Footer
    """
    def breadcrumbs(self):
        """ Breadcrumbs
        """
        root = getApplicationRoot(self.context)

        parent = self.context
        breadcrumbs = [parent.Title(),]

        while parent is not root:
            parent = parent.getParentNode()
            breadcrumbs.append(parent.Title())
        return reversed(breadcrumbs)
