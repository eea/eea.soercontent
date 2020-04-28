""" Evolve to version 6.8
"""
import logging
import transaction
from eea.geotags.interfaces import IGeoTags
from plone.api import content
from zope.component import getAdapter
from Products.CMFCore.utils import getToolByName

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

    soer_2010.setTitle(soer_page_2010.Title())
    soer_2010.setDescription(soer_page_2010.Description())
    soer_2010.setEffectiveDate(soer_page_2010.getEffectiveDate())
    soer_2010.setCreationDate(soer_page_2010.creation_date)
    soer_2010.setSubject(soer_page_2010.Subject())
    soer_2010.setCreators(soer_page_2010.Creators())
    soer_2010.changeOwnership(soer_page_2010.getOwner())
    soer_2010.temporalCoverage = soer_page_2010.temporalCoverage

    # Map relatedItems
    forwards = soer_page_2010.getRelatedItems()
    backs = soer_page_2010.getBackReferences()

    if forwards:
        soer_2010.setRelatedItems(forwards)

    for ob in backs:
        related = ob.getRelatedItems()
        related.append(soer_2010)
        ob.setRelatedItems(related)

    # set geotags
    geo_page_2010 = getAdapter(soer_page_2010, IGeoTags)
    geo_2010 = getAdapter(soer_2010, IGeoTags)
    geo_2010._set_tags(geo_page_2010.tags)

    soer_2010._p_changed = True
    soer_2010.reindexObject()
    catalog.reindexObject(soer_2010, update_metadata=True)
    transaction.commit()

    soer = context.restrictedTraverse("/www/SITE/soer")
    content.transition(obj=soer, transition='publish')

    logger.info('Finished tweaking moved soer content ... DONE')
    return 'Done moving'