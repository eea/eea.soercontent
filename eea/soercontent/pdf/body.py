""" PDF View
"""
from logging import getLogger
from bs4 import BeautifulSoup
from zope.component import queryMultiAdapter
from eea.pdf.themes.classical.body import Body as PDFBody
logger = getLogger('eea.soercontent')

class Body(PDFBody):
    """ Custom PDF body
    """
    def fix_description(self, html):
        """ Remove description
        """
        soup = BeautifulSoup(html)
        for description in soup.find_all(
                'div', {'class': 'documentDescription'}):
            description.extract()
        return soup.find_all('html')[0].decode()

    def fix_body_class(self, html):
        """ Append print body class
        """
        soup = BeautifulSoup(html)
        body = soup.find('body')
        body.attrs['class'].append('body-print')
        return soup.find_all('html')[0].decode()

    def fix_title(self, html):
        """ Replace title
        """
        newTitle = queryMultiAdapter(
            (self.context, self.request), name='pdf.title')
        newTitle = BeautifulSoup(newTitle())
        soup = BeautifulSoup(html)
        for title in soup.find_all('h1', {'class': 'documentFirstHeading'}):
            title.replaceWith(newTitle)
        return soup.find_all('html')[0].decode()

    def __call__(self, **kwargs):
        html = super(Body, self).__call__(**kwargs)
        try:
            html = self.fix_body_class(html)
            html = self.fix_description(html)
            html = self.fix_title(html)
        except Exception, err:
            logger.exception(err)
        return html
