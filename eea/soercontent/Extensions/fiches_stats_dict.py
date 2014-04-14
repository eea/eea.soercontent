""" SOER 2015: fiches stats
"""

import string
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.content import ContentHistoryView

def getHistory(context):
    """ get history for a certain object.
    """
    return ContentHistoryView(context, context.REQUEST).fullHistory()

def hasDoneTransition(history, transition_string):
    """ Given history dictionary it returns true if it finds a certain
        transition string in transition title.
    """
    for transition in history:
        if transition['transition_title'].find(transition_string)>-1:
            return True
    return False

def fichesStatsDict(context):
    """ Return a list of dictionary with Fiche statistics.
    """
    cat = getToolByName(context, 'portal_catalog', None)
    #acl_users = getToolByName(context, 'acl_users', None)
    wf  = getToolByName(context, 'portal_workflow', None)
    pubs=cat.searchResults({ 'meta_type' : ['Fiche'],
                             'review_state':['web_editing',
                                             'ready_for_eionet_review',
                                             'visible','published_eionet'],
                                             'path':'/www/SITE/soer-2015/',
                                             'show_inactive': True,
                                              'language':'ALL' })

    fiches = []

    for pub in pubs[:10]:
        pubo = pub.getObject()
        html = pubo.getText()

        #exclude references and endnotes section if present in body text
        ref_section_inbody = 0
        ref_text = ''
        ref_html = ''
        ref_starts = string.find(html,'<h2>References')
        if ref_starts > 0:
            ref_html = html[ref_starts-1:]
            html = html[:ref_starts]
            ref_text = context.html_to_text(context,ref_html)

        #strip all html from text
        text = context.html_to_text(context, html)
        i = 0

        #get all the creators
        contact_author = ''
        authors = []
        contributors = []

        for userid in pub.listCreators:
            #member = acl_users.getUserById(userid)
            # to be changed to a proper PAS method to get full name
            member = ''
            i += 1
            if member:
                if i == 1:
                    contact_author = member.getProperty('cn')
                else:
                    authors.append(member.getProperty('cn'))
            else:
                #if not in ldap
                if i == 1:
                    contact_author = userid
                else:
                    authors.append(userid)

        #get all contributors
        for userid in pubo.Contributors():
            #member = acl_users.getUserById(userid)
            member = ''
            if member:
                contributors.append(member.getProperty('cn'))
            else:
                contributors.append(userid)

        #check history view if it has been copy-edited
        #historyview = pubo.restrictedTraverse('contenthistorypopup')
        history = getHistory(pubo)
        light_copy_edit = ''
        light_web_edit = ''
        light_fig_edit = ''
        if hasDoneTransition(history,'copy-edit done'):
            light_copy_edit = 'yes'
        if hasDoneTransition(history,'Light web edit done'):
            light_web_edit = 'yes'
        if hasDoneTransition(history,'Light visualisation integration done'):
            light_fig_edit = 'yes'

        #textdots = context.html_to_text(context,htmldots)

        # Replace commas, hyphens etc (count them as spaces)
        #txtcls = context.normalise_text(text)

        #characters, #sentences, #words, #flesch-index
        count_characters = len(text)
        count_characters_ref = len(ref_text)
        #count_sentences = context.count_sentences(txtcls)
        #count_words = context.count_words(txtcls)
        #flesch_reading_ease_score = context.flesch_kincaid_reading_ease(txtcls)
        #flesch_kincaid_grade_level = context.flesch_kincaid_grade_level(txtcls)

        #stats about related content
        related_items = pubo.getRelatedItems()
        nr_related_items =  len(related_items)
        nr_ind = 0
        nr_ind_draft = 0
        #DISABLED due to permission issues on certain unpublished
        # objects for SOERCopyEditors group
        for ob in related_items:
            if ob.portal_type == 'Assessment':
                nr_ind += 1
                indState = wf.getInfoFor(ob, 'review_state')
                if indState != 'published':
                    nr_ind_draft += 1

        #nr of figures
        nr_static_figs = html.count('<img')
        nr_daviz = html.count('<iframe')
        nr_figs = nr_static_figs + nr_daviz

        url = pubo.absolute_url()

        fiche = dict(title=pub.Title,
                     contact_author=contact_author,
                     authors=authors,
                     contributors=contributors,
                     light_copy_edit=light_copy_edit,
                     light_web_edit=light_web_edit,
                     light_fig_edit=light_fig_edit,
                     count_characters = count_characters,
                     #count_sentences = count_sentences,
                     #count_words = count_words,
                     #flesch_reading_ease_score = flesch_reading_ease_score,
                     #flesch_kincaid_grade_level = flesch_kincaid_grade_level,
                     nr_ind = nr_ind,
                     nr_ind_draft = nr_ind_draft,
                     nr_figs = nr_figs,
                     nr_static_figs = nr_static_figs,
                     nr_daviz = nr_daviz,
                     nr_related_items = nr_related_items,
                     ref_section_inbody = ref_section_inbody,
                     count_characters_ref = count_characters_ref,
                     review_state = pub.review_state,
                     url = url)

        fiches.append(fiche)

    #print fiches
    #response.setHeader('Content-Type','text/plain; charset=utf-8')
    #cd = 'attachment; filename=fiche_stats.tsv'
    #response.setHeader('Content-Disposition', cd)

    return fiches

    #return printed

