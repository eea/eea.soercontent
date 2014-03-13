""" Evolve to version 1.9
"""
import logging
from Products.CMFCore.utils import getToolByName
logger = logging.getLogger('eea.soercontent')

def fix_mimetypes(context):
    """ Fix new schema fields mimetypes
    """
    ctool = getToolByName(context, 'portal_catalog')
    brains = ctool.unrestrictedSearchResults(portal_type=['Fiche'])

    total = len(brains)
    logger.info('Fixing %s Fiches mimetypes ...', total)

    for brain in brains:

        doc = brain.getObject()

        summary = getattr(doc, 'summary', None)
        if not summary:
            doc.getField('summary').getMutator(doc)(u'')
            summary = getattr(doc, 'summary', None)

        mimetype = getattr(summary, 'mimetype', 'text/html')
        if mimetype != 'text/html':
            logger.info('Fixing summary for %s', brain.getURL())
            setattr(summary, 'mimetype', 'text/html')

        endnotes = getattr(doc, 'endnotes', None)
        if not endnotes:
            doc.getField('endnotes').getMutator(doc)(u'')
            endnotes = getattr(doc, 'endnotes', None)

        mimetype = getattr(endnotes, 'mimetype', 'text/html')
        if mimetype != 'text/html':
            logger.info('Fixing endnotes for %s', brain.getURL())
            setattr(endnotes, 'mimetype', 'text/html')

    logger.info('Fixing Fiches mimetypes ... DONE')
    return 'Done fixing %s' % total
