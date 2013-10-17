""" Definition of the Glossary content type
"""
from zope.interface import implements
from eea.soercontent.interfaces import IGlossary
from eea.soercontent.content.schema import SoerContent

class Glossary(SoerContent):
    """ Glossary """

    implements(IGlossary)
    meta_type = "Glossary"
    portal_type = "Glossary"
    archetypes_name = "Glossary"
    schema = SoerContent.schema.copy()
