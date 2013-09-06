"""Definition of the Glossary content type
"""

from zope.interface import implements

from Products.ATContentTypes.content import document
from Products.ATContentTypes.content import schemata

from eea.soercontent.interfaces import IGlossary
from eea.soercontent.content.schema import SCHEMA

GlossarySchema = document.ATDocumentSchema.copy() + SCHEMA.copy()

schemata.finalizeATCTSchema(
    GlossarySchema,
    folderish=True,
    moveDiscussion=False
)


class Glossary(document.ATDocument):
    """ Glossary """

    implements(IGlossary)

    meta_type = "Glossary"
    portal_type = "Glossary"
    archetypes_name = "Glossary"

    schema = GlossarySchema
