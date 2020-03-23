""" Evolve to version 6.5
"""
import logging
import transaction
from plone.api import content
from Products.CMFCore.utils import getToolByName
logger = logging.getLogger('eea.soercontent')


def move_soer_content(context):
    """ Move relevant soer content under /soer
    """
    ctool = getToolByName(context, 'portal_catalog')

    soer_2015 = context.restrictedTraverse("/www/SITE/soer-2015")
    soer_2020 = context.restrictedTraverse("/www/SITE/soer-2020")
    soer = context.restrictedTraverse("/www/SITE/soer") 

    new_soer_2015 = content.move(soer_2015, soer, '2015')
    new_soer_2020 = content.move(soer_2020, soer, '2020')
    default_page = context.restrictedTraverse("/www/SITE/soer/2020/soer-2020")
    default_page = content.move(default_page, soer, 'soer-2020')

    logger.info('Finished moving soer content ... DONE')
    return 'Done moving'

def tweak_moved_items(context):
    """ Minor fixes to the moved soer items above
    """
    collections_2015 = context.restrictedTraverse("/www/SITE/soer/2015/collections")
    for name, collection in collections_2015.objectItems():
        if collection.portal_type != 'Collection':
            continue
        for query in collection.query:
            if query.get('i', None) == 'path':
                if 'soer-2015' in query['v']:
                    logger.info('Replacing search location for %s' % collection.absolute_url)
                    query.v = query.v.replace('soer-2015', 'soer/2015')
                    collection._p_changed = True
                    collection.reindexObject()
    logger.info('Finished tweaking soer content ... DONE')
    return 'Done tweaking'
