""" Public interfaces
"""
# Browser layer
from eea.soercontent.browser.interfaces import ILayer

# Content
from eea.soercontent.content.interfaces import ISoerContent
from eea.soercontent.content.interfaces import IFiche
from eea.soercontent.content.interfaces import IInfographic
from eea.soercontent.content.interfaces import IGlossary

__all__ = [
    ILayer.__name__,
    ISoerContent.__name__,
    IFiche.__name__,
    IInfographic.__name__,
    IGlossary.__name__,
]
