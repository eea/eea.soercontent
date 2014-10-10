""" Custom viewlets
"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common


class Disclaimer(common.ViewletBase):
    """ Custom viewlet for qr box
    """
    render = ViewPageTemplateFile('zpt/disclaimer.viewlet.pt')

    @property
    def available(self):
        """ Available
        """
        if getattr(self.context, 'portal_type', '') != 'Fiche':
            return False

        field = self.context.getField('disableDisclaimer')
        disabled =  field.getAccessor(self.context)() if field else False
        if disabled:
            return False

        return True
