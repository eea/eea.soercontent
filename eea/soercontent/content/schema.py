""" Custom schema
"""
from zope.interface import implements
from Products.Archetypes import atapi
from plone.app.blob.field import ImageField
from eea.soercontent.config import EEAMessageFactory as _
from Products.GenericSetup.interfaces import IDAVAware
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import document
from eea.soercontent.content.interfaces import ISoerContent


SCHEMA = atapi.Schema((
    atapi.TextField("summary",
          schemata="default",
          required=False,
          default_output_type="text/x-html-safe",
          widget=atapi.RichWidget(
              label=_(u'Key messages (summary)'),
              description=_(u'Please provide a summary, '
                            u'including the key messages, in this section.'),
              rows=10)
    ),
    atapi.TextField("endnotes",
          schemata="default",
          required=False,
          default_output_type="text/x-html-safe",
          widget=atapi.RichWidget(
              label=_(u'References and endnotes'),
              description=_(u'References, endnotes, footnotes, '
                            u'abbreviations and definitions'),
              rows=25)
    ),

    ImageField(
        name="image",
        schemata="default",
        sizes=None,
        widget=atapi.ImageWidget(
            label=_("Image"),
            description=_("Image used for cover, thumbnail and listings")),
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
    atapi.BooleanField(
        name='presentation',
        schemata='settings',
        required=False,
        languageIndependent=True,
        widget=atapi.BooleanWidget(
            label=_(u'Presentation mode'),
            description=_(u"If selected, this will give users the ability to "
                          u"view the contents as presentation slides.")
        )
    ),
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

    schema['description'].widget.label = _(u"Short summary")

    schema.moveField('summary', after="description")

    schema.moveField('endnotes', after='text')
