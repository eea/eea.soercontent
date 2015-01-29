""" PDF Cover classes
"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.pdf.themes.page.cover import Cover as PDFCover
from eea.pdf.themes.page.cover import BackCover as PDFBackCover


class Cover(PDFCover):
    """ Custom PDF cover
    """
    template = ViewPageTemplateFile('soer2015_cover.pt')


class BackCover(PDFBackCover):
    """ PDF Back cover
    """
    template = ViewPageTemplateFile('soer2015_cover_back.pt')
