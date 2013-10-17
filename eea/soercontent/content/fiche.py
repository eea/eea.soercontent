""" Definition of the Fiche content type
"""

from zope.interface import implements
from eea.soercontent.interfaces import IFiche
from eea.soercontent.content.schema import SoerContent

class Fiche(SoerContent):
    """ Fiche """

    implements(IFiche)

    meta_type = "Fiche"
    portal_type = "Fiche"
    archetypes_name = "Fiche"
    schema = SoerContent.schema.copy()
