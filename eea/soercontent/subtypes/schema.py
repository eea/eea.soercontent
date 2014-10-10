""" Schema extender for Disable Autolinks for context/page
"""
from zope.interface import implements, noLongerProvides, alsoProvides
from Products.Archetypes.public import BooleanField, BooleanWidget
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.field import ExtensionField
from eea.soercontent.config import EEAMessageFactory as _
from eea.soercontent.interfaces import ILayer, ICountryFiche


class EEADisableBooleanField(ExtensionField, BooleanField):
    """ BooleanField for schema extender
    """
    def get(self, instance, **kwargs):
        """ Override accessor
        """
        if ICountryFiche.providedBy(instance):
            return False
        return True

    def set(self, instance, value, **kwargs):
        """ Override mutator
        """
        if value:
            if ICountryFiche.providedBy(instance):
                noLongerProvides(instance, ICountryFiche)
        else:
            if not ICountryFiche.providedBy(instance):
                alsoProvides(instance, ICountryFiche)


class EEASchemaExtender(object):
    """ Schema extender for inline comment fields
    """
    implements(ISchemaExtender, IBrowserLayerAwareExtender)
    layer = ILayer

    fields = (
        EEADisableBooleanField(
            name='disableDisclaimer',
            schemata='settings',
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
