""" Upgrade scripts to version 1.4
"""
import logging
from zope.component import queryMultiAdapter
from Products.CMFCore.utils import getToolByName
logger = logging.getLogger('eea.soercontent')

def migrate2folderish(context):
    """ Migrate to folderish
    """
    ctool = getToolByName(context, 'portal_catalog')
    brains = ctool.unrestrictedSearchResults(
        portal_type=['Fiche', 'Glossary', 'Infographic'])

    request = context.REQUEST
    mtool = queryMultiAdapter((context, request), name='migrate-btrees')

    total = len(brains)
    logger.info('Migrating %s SOER ctypes...', total)

    for brain in brains:
        logger.info('Migrating %s', brain.getURL())
        try:
            doc = brain.getObject()
            mtool.migrate(doc)
        except Exception, err:
            logger.warn("Couldn't migrate %s", brain.getURL())
            logger.exception(err)
            continue

    logger.info('Migrating SOER ctypes... DONE')
    return 'Done migrating %s' % total
