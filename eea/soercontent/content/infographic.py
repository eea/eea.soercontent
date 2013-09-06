"""Definition of the Infographic content type
"""

from zope.interface import implements

from Products.ATContentTypes.content import document
from Products.ATContentTypes.content import schemata

from eea.soercontent.interfaces import IInfographic
from eea.soercontent.content.schema import SCHEMA

InfographicSchema = document.ATDocumentSchema.copy() + SCHEMA.copy()


schemata.finalizeATCTSchema(
    InfographicSchema,
    folderish=True,
    moveDiscussion=False
)


class Infographic(document.ATDocument):
    """ Infographic """

    implements(IInfographic)

    meta_type = "Infographic"
    portal_type = "Infographic"
    archetypes_name = "Infographic"

    schema = InfographicSchema
