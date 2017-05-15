""" PDF View
"""
from logging import getLogger
from Acquisition import aq_base
from Products.CMFPlone.utils import safe_hasattr
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.pdf.themes.page.body import Body as PDFBody
from eea.pdf.themes.book.folder import Body as FolderBody


logger = getLogger('eea.soercontent')


class Body(PDFBody):
    """ Custom PDF body
    """
    template = ViewPageTemplateFile('body.pt')

    def __call__(self, **kwargs):
        self.request.set('skipRelations', 1)
        return self.template()


class Soer2015Body(FolderBody):
    """ Soer2015 folder custom body
    """
    template = ViewPageTemplateFile('soer2015_body.pt')

    @property
    def brains(self):
        """ Brains of collections or folderish content
        """
        if safe_hasattr(aq_base(self.context), 'queryCatalog'):
            return self.context.queryCatalog(batch=False)[:self.maxbreadth]
        else:
            return self.context.getFolderContents()[:self.maxbreadth]
