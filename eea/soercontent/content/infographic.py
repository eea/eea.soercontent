""" Definition of the Infographic content type
"""

from zope.interface import implements
from eea.soercontent.interfaces import IInfographic
from eea.soercontent.content.schema import SoerContent

class Infographic(SoerContent):
    """ Infographic """

    implements(IInfographic)

    meta_type = "Infographic"
    portal_type = "Infographic"
    archetypes_name = "Infographic"

    schema = SoerContent.schema.copy()
