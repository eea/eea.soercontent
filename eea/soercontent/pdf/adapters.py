""" PDF Adapters
"""
class OptionsMaker(object):
    """ PDF Converter for SOER content-types
    """
    def __init__(self, context):
        self.context = context

    def overrideAll(self):
        """ Override all options
        """
        return True

    def getOptions(self):
        """ Custom options
        """
        return {
            'cover': self.context.absolute_url() + '/fiche_cover',
            'header-right': self.context.title_or_id(),
            'footer-left': '[page] [section]' ,
            'footer-right': '[subsection]',
            'footer-line': 1,
            'header-line': 1,
            'page-size': 'A4',
            'margin-top': '20',
            'margin-bottom': '20',
            'margin-left': '20',
            'margin-right': '20',
        }
