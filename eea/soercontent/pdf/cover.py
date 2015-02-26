""" PDF Cover classes
"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.pdf.themes.page.cover import Cover as PDFCover
from eea.pdf.themes.page.cover import BackCover as PDFBackCover
from eea.soercontent.pdf.utils import split_root_title


class Cover(PDFCover):
    """ Custom PDF cover
    """
    template = ViewPageTemplateFile('soer2015_cover.pt')

    def has_cover_image(self):
        """
        :return:
        :rtype:
        """
        context = self.context
        image = context.getField('coverImage')
        return image.get_size(context) != 0 if image else False

    def get_children_cover_images(self):
        """
        :return:
        :rtype:
        """
        briefings = self.context.getFolderContents(
            {"portal_type": "Fiche", "sort_limit": 3,
             "sort_on": "getObjPositionInParent"})
        briefings = [b.getObject() for b in briefings]
        return briefings

    @property
    def header(self):
        """
        :rtype : object
        """
        return split_root_title(self.context, start_slice_from=1)


class BackCover(PDFBackCover):
    """ PDF Back cover
    """
    template = ViewPageTemplateFile('soer2015_cover_back.pt')
