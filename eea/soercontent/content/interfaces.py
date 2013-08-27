""" Content interfaces

   >>> portal = layer['portal']
   >>> sandbox = portal['sandbox']

"""
from zope.interface import Interface

class IFiche(Interface):
    """ Fiche

        >>> fid = sandbox.invokeFactory('Fiche', id='Fiche')
        >>> doc = sandbox._getOb(fid)
        >>> doc
        <Fiche at...>

    """

class IInfographic(Interface):
    """ Infographic

        >>> fid = sandbox.invokeFactory('Infographic', id='Infographic')
        >>> doc = sandbox._getOb(fid)
        >>> doc
        <Infographic at...>

    """

class IGlossary(Interface):
    """ Glossary

        >>> fid = sandbox.invokeFactory('Glossary', id='Glossary')
        >>> doc = sandbox._getOb(fid)
        >>> doc
        <Glossary at...>

    """
