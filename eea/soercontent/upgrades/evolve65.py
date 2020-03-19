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
    default_page = context.restrictedTraverse("/www/SITE/soer-2020/soer-2020")
    soer = context.restrictedTraverse("/www/SITE/soer") 

    new_soer_2015 = content.move(soer_2015, soer, '2015')
    new_soer_2020 = content.move(soer_2020, soer, '2020')
    default_page = content.move(default_page, soer, 'soer-2020')

    logger.info('Finished moving soer content ... DONE')
    return 'Done moving'