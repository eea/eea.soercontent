""" Custom schema
"""
from Products.Archetypes import atapi
from eea.soercontent.config import EEAMessageFactory as _

SCHEMA = atapi.Schema((
    atapi.LinesField(
        name='temporalCoverage',
        schemata="categorization",
        languageIndependent=True,
        required=True,
        multiValued=1,
        vocabulary_factory=u"Temporal coverage",
        widget=atapi.MultiSelectionWidget(
            macro="temporal_widget",
            helper_js=("temporal_widget.js",),
            size=15,
            label=_("Temporal coverage"),
            description=_(
                "The temporal scope of the content of the data "
                "resource. Temporal coverage will typically include "
                "a set of years or time ranges."),
            i18n_domain='eea',
        )
    ),
))
