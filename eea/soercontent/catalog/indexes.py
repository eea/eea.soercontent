""" Custom zCatalog indexes
"""
import logging
from zope.interface import Interface
from plone.indexer.decorator import indexer
from Products.CMFCore.utils import getToolByName
logger = logging.getLogger('eea.soercontent')

@indexer(Interface)
def review_title(obj, **kwargs):
    """ Index for review state title
    """
    try:
        wftool = getToolByName(obj, 'portal_workflow')
        review_state = wftool.getInfoFor(obj, 'review_state')
        return wftool.getTitleForStateOnType(review_state, obj.portal_type)
    except Exception, err:
        logger.debug(err)
        raise AttributeError
