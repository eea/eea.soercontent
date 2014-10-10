""" Schema extender for Disable Autolinks for context/page
"""
from zope.interface import implements
from Products.Archetypes.public import BooleanField, BooleanWidget
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.field import ExtensionField
from eea.soercontent.config import EEAMessageFactory as _
from eea.soercontent.interfaces import ILayer

class EEABooleanField(ExtensionField, BooleanField):
    """ BooleanField for schema extender
    """

class EEASchemaExtender(object):
    """ Schema extender for inline comment fields
    """
    implements(ISchemaExtender, IBrowserLayerAwareExtender)
    layer = ILayer

    fields = (
        EEABooleanField(
            name='disableDisclaimer',
            schemata='settings',
            default=True,
            searchable=False,
            widget=BooleanWidget(
                label=_('Disable disclaimer'),
                description=_("Hide country disclaimer for this context"),
            )
        ),
    )

    def __init__(self, context):
        self.context = context

    def getFields(self):
        """ Returns fields
        """
        return self.fields
