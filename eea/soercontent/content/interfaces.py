""" Content interfaces

   >>> portal = layer['portal']
   >>> sandbox = portal['sandbox']

"""
from zope.interface import Interface
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

class ICountryFiche(Interface):
    """ Marker interface for Country Fiches
    """
