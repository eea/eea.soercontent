"""Definition of the Fiche content type
"""

from zope.interface import implements

from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from eea.soercontent.interfaces import IFiche
from eea.soercontent.content.schema import SCHEMA

FicheSchema = folder.ATFolderSchema.copy() + SCHEMA.copy()

schemata.finalizeATCTSchema(
    FicheSchema,
    folderish=True,
    moveDiscussion=False
)

class Fiche(folder.ATFolder):
    """ Fiche """

    implements(IFiche)

    meta_type = "Fiche"
    portal_type = "Fiche"
    archetypes_name = "Fiche"

    schema = FicheSchema
