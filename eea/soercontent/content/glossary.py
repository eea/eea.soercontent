"""Definition of the Glossary content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from eea.soercontent.interfaces import IGlossary

GlossarySchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(
    GlossarySchema,
    folderish=True,
    moveDiscussion=False
)


class Glossary(folder.ATFolder):
    """ Glossary """

    implements(IGlossary)

    meta_type = "Glossary"
    portal_type = "Glossary"
    archetypes_name = "Glossary"

    schema = GlossarySchema
