""" PDF Cover classes
"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.pdf.themes.page.cover import Cover as PDFCover
from eea.pdf.themes.page.cover import BackCover as PDFBackCover


class Cover(PDFCover):
    """ Custom PDF cover
    """
    template = ViewPageTemplateFile('soer2015_cover.pt')

    def has_cover_image(self):
        """
        :return:
        :rtype:
        """
        return self.context.coverImage.width

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


class BackCover(PDFBackCover):
    """ PDF Back cover
    """
    template = ViewPageTemplateFile('soer2015_cover_back.pt')
