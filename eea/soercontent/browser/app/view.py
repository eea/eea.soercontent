""" eea.soercontent Browser Views
"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.Five.browser import BrowserView


class FicheView(BrowserView):
    """ FicheView browser page
    """
    index = ViewPageTemplateFile('../zpt/fiche_view.pt')

    @property
    def macros(self):
        """ Implement macros directly on the BrowserView otherwise we don't get
            any preview of content when using versions_history_form page
        """
        return self.index.macros
