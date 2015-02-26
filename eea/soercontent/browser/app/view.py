""" eea.soercontent Browser Views
"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.Five.browser import BrowserView
from plone.memoize.view import memoize


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

    def __call__(self, **kwargs):
        return self.index()


class SOERContentView(BrowserView):
    """ Content browser page
    """

    def __init__(self, context, request):
        super(SOERContentView, self).__init__(context, request)

    def get_parent(self, parent_id=None):
        """
        :param parent_id: string id used for searching the portal_catalog
        :return: :rtype: list of brains
        """
        return self.context.portal_catalog(id=parent_id)

    @memoize
    def content(self, parent_id=None, object_id=None, ptype=None):
        """
        :param ptype: optional portal_type for catalog search
        :param parent_id:
        :param object_id:
        :return: list of dicts with title and url of given ptypes
        :rtype: list
        """
        parent = self.get_parent(parent_id)
        if not parent:
            return []
        obj = parent[0].getObject().restrictedTraverse(object_id, None)
        if not obj:
            return []
        children = self.context.portal_catalog(
            {'path': '/'.join(obj.getPhysicalPath()), 'depth': 1},
            portal_type=ptype or 'Fiche',
            sort_on="getObjPositionInParent")
        return children



