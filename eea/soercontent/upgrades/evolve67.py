""" Evolve to version 6.5
"""
import logging
import transaction
from eea.versions.interfaces import IVersionControl
from eea.versions.versions import assign_version
from plone.api import content
from Products.CMFCore.utils import getToolByName
logger = logging.getLogger('eea.soercontent')


def move_content_in_soer(context):
    """ Move relevant soer content under /soer
    """
    ctool = getToolByName(context, 'portal_catalog')
    soer = context.restrictedTraverse("/www/SITE/soer") 
    soer_2015 = context.restrictedTraverse("/www/SITE/soer/2015")
    soer_2020 = context.restrictedTraverse("/www/SITE/soer/2020")
    soer_intro = context.restrictedTraverse("/www/SITE/soer/intro")

    soer_2010 = content.create(
        type='Folder', title='2010', id='2010-folder', container=soer)
    path = "/www/SITE/soer/"
    vers_dict = {}
    brains = ctool.searchResults(path=path, Language="all")
    for brain in brains:
        obj = brain.getObject()
        try:
            control = IVersionControl(obj)
        except:
            continue
        version_id = control.getVersionId() or None

        uuid = content.get_uuid(obj=obj)
        vers_dict.update({uuid: version_id})  

    created_2010 = ['synthesis', 'europe-and-the-world', 'europe', 'countries',
                    'launches-and-events', 'policy-makers', 'journalists',
                    'page_logo', 'advanced-search', 'Cover4ebook1page.jpg',
                    'soer_video', 'vnr', 'soer-logo', 'assessments',
                    'video-norway-2013-in-partnership', 'soer-structure-mini',
                    'italy-environmental-data-yearbook-multimedia-edition',
                    'soer-structure-overview', 'unpublished-content', 
                    'latest-changes', 'published-future', 
                    'part-c-content-monitoring', 'all-key-facts']
    ignore = [soer_2010, soer_2015, soer_2020, soer_intro]
    for soer_content in soer.listFolderContents():
        if soer_content in ignore:
            continue
        if '2010' in soer_content.id or '2010' in soer_content.title or soer_content.id in created_2010:
            content.move(soer_content, soer_2010)
        elif '2015' in soer_content.id or '2015' in soer_content.title:
            content.move(soer_content, soer_2015)
        elif '2020' in soer_content.id or '2020' in soer_content.title:
            content.move(soer_content, soer_2020)

    path = "/www/SITE/soer"
    brains = ctool.searchResults(path=path, Language="all")
    for brain in brains:
        obj = brain.getObject()
        try:
            control = IVersionControl(obj)
        except:
            continue

        version_id = control.getVersionId() or None
        uuid = content.get_uuid(obj=obj)
        if vers_dict.get(uuid, None):
            if vers_dict.get(uuid, None) == version_id:
                logger.info('GOOD OBJECT %s' % obj.absolute_url())
            else:
                logger.info('BAD OBJECT %s' % obj.absolute_url())
                control.setVersionId(vers_dict.get(uuid))
                obj._p_changed = True
                obj.reindexObject()
                transaction.commit()
            del vers_dict[uuid]
    logger.info('Finished moving soer content ... DONE')
    return 'Done moving'
    

def tweaks(context):
    """ Soer content tweaks
    """
    soer_2010 = context.restrictedTraverse("/www/SITE/soer/2010-1")
    soer_2015 = context.restrictedTraverse("/www/SITE/soer/2015")

    # set default page
    soer_2010.default_page = '2010'
    soer_2010._p_changed = True
    soer_2010.reindexObject()

    assign_version(soer_2015, 'KUPLUPKOKLU888')
    content.rename(obj=soer_2010, new_id='2010')
    content.transition(obj=soer_2010, transition='publish')

    logger.info('Finished tweaking moved soer content ... DONE')
    return 'Done moving'