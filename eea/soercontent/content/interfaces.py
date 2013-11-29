""" Content interfaces

   >>> portal = layer['portal']
   >>> sandbox = portal['sandbox']

"""
try:
    from Products.EEAContentTypes.interfaces import IEEAContent as Interface
except ImportError:
    from zope.interface import Interface
from Products.ATContentTypes.interfaces import IATDocument

class ISoerContent(IATDocument, Interface):
    """ Abstract interface for all SOER Content-Types
    """

class IFiche(ISoerContent):
    """ Fiche

        >>> fid = sandbox.invokeFactory('Fiche', id='Fiche')
        >>> doc = sandbox._getOb(fid)
        >>> doc
        <Fiche at...>

    """

class IGlossary(ISoerContent):
    """ Glossary

        >>> fid = sandbox.invokeFactory('Glossary', id='Glossary')
        >>> doc = sandbox._getOb(fid)
        >>> doc
        <Glossary at...>

    """
