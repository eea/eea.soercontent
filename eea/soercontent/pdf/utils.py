""" Pdf utils
"""

from eea.pdf.utils import getApplicationRoot


def root_title(context):
    """
    :param context: object
    :return: Application root title or string
    :rtype: str
    """
    root = getApplicationRoot(context)
    title = root.title_or_id()
    return title


def split_root_title(context, only_first_slice=False,
                     start_slice_from=None, stop_slice_at=None):
    """
    :param context:
    :type context: object
    :return: Splitted title stripped of whitespace
    :rtype: str
    """
    title = root_title(context)
    # split title on em dashes if matched
    # else returns original string wrapped
    # within a list
    splitted_title = title.split("\xe2\x80\x94")
    title_len = len(splitted_title)
    stripped_title = [o.strip() for o in splitted_title]
    if title_len == 1 or only_first_slice:
        return splitted_title[0]
    h_start_from = start_slice_from is not None
    h_stop_at = stop_slice_at is not None
    if h_start_from:
        if start_slice_from == stop_slice_at:
            return stripped_title[start_slice_from]
        if not h_stop_at:
            return stripped_title[start_slice_from:]
    if h_stop_at and not h_start_from:
        return stripped_title[:stop_slice_at]
    if h_stop_at and h_start_from:
        return stripped_title[start_slice_from:stop_slice_at]
    return stripped_title
