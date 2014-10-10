""" Custom viewlets
"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common
from eea.soercontent.interfaces import ICountryFiche


class Disclaimer(common.ViewletBase):
    """ Custom viewlet for qr box
    """
    render = ViewPageTemplateFile('zpt/disclaimer.viewlet.pt')

    @property
    def available(self):
        """ Available
        """
        if ICountryFiche.providedBy(self.context):
            return True
        return False
