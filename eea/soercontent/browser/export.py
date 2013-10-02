""" Export as epub
"""


from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from eea.epub.browser.export import ExportView

class EPubView(ExportView):
    """ EPubView Browserview
    """
    template = ViewPageTemplateFile('zpt/epub.pt')
