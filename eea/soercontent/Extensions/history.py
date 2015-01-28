from zope.component import getMultiAdapter

def history(obj):
    """ History """
    request = obj.REQUEST
    view = getMultiAdapter((obj, request), name='contenthistory')
    return view.workflowHistory()

