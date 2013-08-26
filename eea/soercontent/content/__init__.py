""" Custom content
"""
from Products.ATContentTypes.content.base import registerATCT
from eea.soercontent.content.fiche import Fiche
from eea.soercontent.config import PROJECTNAME

def register():
    """ Register custom content-types
    """
    registerATCT(Fiche, PROJECTNAME)
