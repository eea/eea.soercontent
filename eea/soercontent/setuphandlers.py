""" Various setup
"""
import logging
from Products.CMFCore.utils import getToolByName
logger = logging.getLogger('eea.soercontent')

def setupVarious(context):
    """ Do some various setup.
    """
    if context.readDataFile('eea.soercontent.txt') is None:
        return

    atool = getToolByName(context, 'portal_atct')
    if not atool:
        return

    if 'review_title' not in atool.topic_metadata:
        logger.info('Adding topic metadata review_title within portal_atct')
        atool.addMetadata('review_title', friendlyName='State (title)',
                          enabled=True)
