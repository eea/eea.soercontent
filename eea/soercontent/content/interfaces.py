""" Content interfaces

   >>> portal = layer['portal']
   >>> sandbox = portal['sandbox']

"""
from Products.ATContentTypes.interfaces import IATDocument

class ISoerContent(IATDocument):
    """ Abstract interface for all SOER Content-Types
    """

class IFiche(ISoerContent):
    """ Fiche

        >>> fid = sandbox.invokeFactory('Fiche', id='Fiche')
        >>> doc = sandbox._getOb(fid)
        >>> doc
        <Fiche at...>

    """

class IInfographic(ISoerContent):
    """ Infographic

        >>> fid = sandbox.invokeFactory('Infographic', id='Infographic')
        >>> doc = sandbox._getOb(fid)
        >>> doc
        <Infographic at...>

    """

class IGlossary(ISoerContent):
    """ Glossary

        >>> fid = sandbox.invokeFactory('Glossary', id='Glossary')
        >>> doc = sandbox._getOb(fid)
        >>> doc
        <Glossary at...>

    """
