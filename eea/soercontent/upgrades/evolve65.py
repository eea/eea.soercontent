""" Evolve to version 6.5
"""
import logging
import transaction
from eea.versions.interfaces import IVersionControl
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

    paths = ["/www/SITE/soer-2015", "/www/SITE/soer-2020"]
    vers_dict = {}
    for path in paths:
        brains = ctool.searchResults(path=path, Language="all")

        for brain in brains:
            obj = brain.getObject()
            try:
                control = IVersionControl(obj)
            except:
                continue
            version_id = control.getVersionId() or None

            if obj.id in ['soer-2015', 'soer-2020'] and obj.portal_type == 'Folder':
                logger.info('UPDATING FOLDER %s' % obj.absolute_url())
                vers_dict.update({obj.id.split('-')[-1]: version_id})
            else:
                vers_dict.update({obj.id: version_id})

    content.move(soer_2015, soer, '2015')
    content.move(soer_2020, soer, '2020')
    default_page = context.restrictedTraverse("/www/SITE/soer/2020/soer-2020")
    default_page = content.move(default_page, soer, 'soer-2020')

    paths = ["/www/SITE/soer/2015", "/www/SITE/soer/2020", "/www/SITE/soer/soer-2020"]
    for path in paths:
        brains = ctool.searchResults(path=path, Language="all")

        for brain in brains:
            obj = brain.getObject()
            try:
                control = IVersionControl(obj)
            except:
                continue

            version_id = control.getVersionId() or None
            if vers_dict.get(obj.id, None):
                if vers_dict.get(obj.id, None) == version_id:
                    logger.info('GOOD OBJECT %s' % obj.absolute_url())
                else:
                    logger.info('BAD OBJECT %s' % obj.absolute_url())
                    control.setVersionId(vers_dict.get(obj.id))
                    obj._p_changed = True
                    obj.reindexObject()
                    transaction.commit()

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
                    logger.info('Replacing search location for %s' % collection.absolute_url())
                    query.v = query.v.replace('soer-2015', 'soer/2015')
                    collection._p_changed = True
                    collection.reindexObject()
    logger.info('Finished tweaking soer content ... DONE')
    return 'Done tweaking'
