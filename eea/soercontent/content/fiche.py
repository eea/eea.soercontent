"""Definition of the Fiche content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from eea.soercontent.content.interfaces import IFiche

FicheSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(
    FicheSchema,
    folderish=True,
    moveDiscussion=False
)


class Fiche(folder.ATFolder):
    """Fiche"""
    implements(IFiche)

    meta_type = "Fiche"
    schema = FicheSchema
