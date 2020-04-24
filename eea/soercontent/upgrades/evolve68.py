""" Evolve to version 6.8
"""
import logging
import transaction
from plone.api import content
from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility
from Products.ATContentTypes.interface import IATCTTool
from eea.versions.interfaces import IVersionControl
from eea.versions.versions import assign_version


logger = logging.getLogger('eea.soercontent')


def tweaks(context):
    """ Additional soer content tweaks
    """
    catalog = getToolByName(context, 'portal_catalog')
    soer_2010 = context.restrictedTraverse("/www/SITE/soer/2010")
    soer_page_2010 = context.restrictedTraverse("/www/SITE/soer/2010/2010")
    
    page_keys = soer_page_2010.Schema().keys()
    folder_keys = soer_2010.Schema().keys()
    for key in page_keys:
        field = soer_page_2010.getField(key)
        if not field:
            continue

        value = field.getAccessor(soer_page_2010)()
        # Fix some metadata
        if key in folder_keys:
            setattr(soer_2010, key, value)

    atool = queryUtility(IATCTTool)
    metadata = atool.getAllMetadata(True)
    brain_2010 = catalog.searchResults(path={'query': '/www/SITE/soer/2010', 'depth': 0})[0]
    brain_page_2010 = catalog.searchResults(path={'query': '/www/SITE/soer/2010/2010', 'depth': 0})[0]

    metadata += ['geotags', 'effective', 'created']
    for key in metadata:
        try:
            value = getattr(brain_page_2010, key)
            setattr(brain_2010, key, value)
        except:
            continue

    soer_2010.effective_date = soer_page_2010.effective_date
    # control = IVersionControl(soer_page_2010)
    # version_id = control.getVersionId() or None
    # assign_version(soer_2010, version_id)

    soer_2010._p_changed = True
    soer_2010.reindexObject()
    # catalog.unindexObject(soer_2010)
    catalog.reindexObject(soer_2010, update_metadata=True)
    transaction.commit()
    soer = context.restrictedTraverse("/www/SITE/soer")
    content.transition(obj=soer, transition='publish')
    logger.info('Finished tweaking moved soer content ... DONE')
    return 'Done moving'