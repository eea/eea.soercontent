""" Custom schema
"""
from zope.interface import implements
from Products.Archetypes import atapi
from eea.soercontent.config import EEAMessageFactory as _
from Products.GenericSetup.interfaces import IDAVAware
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import document
from eea.soercontent.content.interfaces import ISoerContent

SCHEMA = atapi.Schema((
    atapi.ImageField(
        name="image",
        schemata="default",
        sizes=None,
        widget=atapi.ImageWidget(
            label=_("Thumbnail"),
            description=_("Image for thumbnail")),
            i18n_domain='eea',
        ),
    atapi.StringField(
        name='imageCopyright',
        schemata="default",
        widget=atapi.StringWidget(
            label=_("Image Copyright"),
            description=_("Enter the copyright information for this image."),
            i18n_domain='eea',
        )
    ),
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
    atapi.TextField(
        name='license',
        schemata="creators",
        allowable_content_types=('text/plain',),
        widget=atapi.TextAreaWidget(
            label=_(u'License'),
            description=_(u'License information')
        )
    ),
    atapi.TextField(
        name='publisher',
        schemata="creators",
        allowable_content_types=('text/plain',),
        widget=atapi.TextAreaWidget(
            label=_(u'Publisher'),
            description=_(u'Publisher information')
        )
    ),
    atapi.BooleanField(
        schemata='settings',
        name='presentation',
        required=False,
        languageIndependent=True,
        widget=atapi.BooleanWidget(
            label=_(u'Presentation mode'),
            description=_(u"If selected, this will give users the ability to "
                          u"view the contents as presentation slides.")
        )
    )
))

class SoerContent(folder.ATFolder, document.ATDocumentBase):
    """ Abstract SOER content-type
    """
    implements(ISoerContent, IDAVAware)

    assocFileExt = ('txt', 'stx', 'rst', 'rest', 'py',)
    assocMimetypes = ('application/xhtml+xml', 'message/rfc822', 'text/*',)

    schema = (
        folder.ATFolderSchema.copy() +
        document.ATDocumentSchema.copy() +
        SCHEMA.copy()
    )
