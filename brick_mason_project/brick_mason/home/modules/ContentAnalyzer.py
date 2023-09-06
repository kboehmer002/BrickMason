'''======================================== Content Analyzer ========================================'''
'''
This module contains processes for search and analysis of bricks for determining content matching to
user search parameters. Determines information to be extracted and inserted into draft bricks in new
Brick generation.
'''
'''============================================ Includes ==========================================='''

from home.models import SourceFile as sf, KTOPS, ContradictionList as cl, RedundantList as rl, SearchResult as sr, TermList, Brick
from home.modules.SourceImporter import extract_from_docx
from django.db.models import Q

'''======================================= Search Database ========================================='''
'''Access RDS tables for adding, modifying, or removing data.                                       '''

''' returns a filtered query of SourceFile objects based on passed parameters. '''
def query_SourceFiles(exts, sDate, eDate, wc_min, wc_max):

    # Filter by wordcount
    if (wc_min is None):
        wc_min = 0
    if (wc_max is None):
        queryset = sf.objects.filter(word_count__gte=wc_min)
    else:
        queryset = sf.objects.filter(word_count__range=[wc_min, wc_max])
    
    # Filter queryset by date range
    if (sDate != None) and (eDate != None):
        queryset = queryset.filter(date_modified__range=[sDate, eDate])
    elif (sDate != None) and (eDate is None):
        # greater than start date
        queryset = queryset.filter(date_modified__gt=sDate)
    elif (sDate is None) and (eDate != None):
        # less than end date
        queryset = queryset.filter(date_modified__lt=eDate)

    # all exts return queryset, else filter by tuple of required size.
    if '1' in exts:
        return queryset
    else:
        count = len(exts)
        
        # Change set of numbers to extensions.
        for i in range(0, len(exts)):
            if (exts[i] == '2'):
                exts[i] = ".docx"
            if (exts[i] == '3'):
                exts[i] = ".png"
            if (exts[i] == '4'):
                exts[i] = ".jpg"
        
        # Filter by extension
        match count:
            case 1:
                queryset = queryset.filter(file__endswith=(exts[0]))
                return queryset
            case 2:
                queryset = queryset.filter(Q(file__endswith=exts[0]) |
                                           Q(file__endswith=exts[1]))
                return queryset
            case 3:
                queryset = queryset.filter(Q(file__endswith=exts[0]) |
                                           Q(file__endswith=exts[1]) |
                                           Q(file__endswith=exts[2]))
                return queryset
            case _:
                return queryset

# ----------------------------------------------------------------------------------------------------------------


''' Removes user's search terms to TermList db table, tracks terms to references.'''
def clear_term_list(username):
    # check user has no terms stored if so,
    # remove them all from the TermList.
    past_results = TermList.objects.filter(bid=None, username=username)
    if past_results.exists():
        for rec in TermList.objects.all():
            # Delete all records not attached to a brick.
            if ((rec.bid is None) and (rec.username == username)):
                rec.delete()

''' Save user's search terms to TermList db table, tracks terms to references.'''
def prep_term_list(record, termList, username):    
    for term in termList:
        # Save current term list into the db TermList table.
        t_record = TermList(rid_id=record.pk, bid=None, username=username,
                            term=term, word_count=0)
        t_record.save()

# ----------------------------------------------------------------------------------------------------------------

''' Saves current search query result in db. Checks if previous
    search result is in db and replaces with new search results
    if so. '''
def save_search_result(query_result, username):
    # check user has no search results stored
    # is so, remove them allfrom SearchResults.
    past_results = sr.objects.filter(username=username)
    if past_results.exists():
        for record in sr.objects.all():
            if (record.username == username):
                record.delete()

    if query_result is None:
        return

    # Save current results to search result table.
    for record in query_result:
        s_item = sr(username=username, fid_id=record.pk)
        s_item.save()

# ----------------------------------------------------------------------------------------------------------------

''' Returns search results stored for username as queryset. '''
def get_search_result(username):
    return sr.objects.filter(username=username)

# ----------------------------------------------------------------------------------------------------------------

''' Returns search results stored for username as queryset. '''
def get_user_bricks(username):
    return Brick.objects.filter(uid=username)

# ----------------------------------------------------------------------------------------------------------------

''' Returns search results stored for username as queryset. '''
def get_SME_bricks(username):
    return Brick.objects.filter(stage='2')

# ----------------------------------------------------------------------------------------------------------------

''' Returns search results stored for username as queryset. '''
def get_Editor_bricks(username):
    return Brick.objects.filter(stage='3')

# ----------------------------------------------------------------------------------------------------------------

''' Returns expanded queryset for listing search results on page.
    eg.) QuerySet [{'fid__file': 'testdoc2.docx', 'fid__title': 
    'testdoc2', 'fid__date_modified': datetime.date(2023, 3, 28),
    'fid__word_count': 71}] '''
def get_display_list(queryset):
    search_list = queryset.select_related('fid').all().order_by(
        'fid__title').values('fid', 'fid__file', 'fid__title', 'fid__date_modified', 'fid__word_count')
        
    return search_list

# ----------------------------------------------------------------------------------------------------------------

''' Takes queryset and toggles order of title if title was the last
    field ordered by. Else, orders queryset by title ascending. '''
def toggle_order_title(queryset, state):
    if state == 't+':
        search_list = queryset.all().order_by('-fid__title')
        state = "t-"
    else:
        search_list = queryset.all().order_by('fid__title')
        state = "t+"
    
    return search_list

# ----------------------------------------------------------------------------------------------------------------

''' Takes queryset and toggles order of date modified, if date modified was
    the last field ordered by. Else, orders queryset by title ascending. '''
def toggle_order_date_modified(queryset, state):
    if state == 'd+':
        search_list = queryset.all().order_by('-fid__date_modified')
        state = "d-"
    else:
        search_list = queryset.all().order_by('fid__date_modified')
        state = "d+"

    return search_list

# ----------------------------------------------------------------------------------------------------------------

''' Takes queryset and toggles order of date modified, if date modified was
    the last field ordered by. Else, orders queryset by title ascending. '''
def toggle_order_word_count(queryset, state):
    if state == 'w+':
        search_list = queryset.all().order_by('-fid__word_count')
        state = "w-"
    else:
        search_list = queryset.all().order_by('fid__word_count')
        state = "w+"

    return search_list

# ----------------------------------------------------------------------------------------------------------------

# Removes the user selected item from the search results list.
def remove_from_list(display_list, file, username):
    # remove file from search results/
    title = file.split('.')[0].replace("_", " ")
    past_results = sr.objects.get(
        username=username, fid__title=title)
    past_results.delete()
    
    #remove file from display list.
    display_list = display_list.exclude(fid__file=file)
    return display_list

'''============================================ Search ============================================'''

'''Function to compare two sets of word (use to compare user query to AWS generated keywords) - returns set of matching words'''
def searchForKeyPhraseMatch(userQueryWordSet, documentKeyWordSet):
    keyWordMatches = userQueryWordSet.intersection(documentKeyWordSet)
    return keyWordMatches

# ----------------------------------------------------------------------------------------------------------------

'''returns list of term_list (user term list) that match at least part of k_list (ktops table list)'''
def return_parts_of(term_list, k_list):
    return [ele2 for ele2 in term_list if any(
        ele2.lower() in ele1.lower() for ele1 in k_list)]

# ----------------------------------------------------------------------------------------------------------------

'''Returns the percent of query words found within the doc's keywords'''
def findPercentMatch(userQueryWordSet, documentKeyWordSet):
    keyWordMatches = searchForKeyPhraseMatch(
        userQueryWordSet, documentKeyWordSet)
    kWM_length = len(keyWordMatches)
    uQWS_length = len(userQueryWordSet)
    percentMatch = (kWM_length/uQWS_length)*100
    return percentMatch

# ----------------------------------------------------------------------------------------------------------------

''' Checks ktops for record analyzed for matches to term list. Checks for
    partial maches of any of the listed items. '''
def check_k_list(term_list, k_list):
    query_word_set = []
    keep = False
    
    # convert queryset to list
    for k in k_list:
        query_word_set.append(k.ktops)

    # keep record if ktops list has a match
    result = return_parts_of(term_list, query_word_set)

    return result

# ----------------------------------------------------------------------------------------------------------------

''' For all listed terms provided by user, perform checks against filtered query.
    Insert and save to SearchResults. '''
def term_search(termList, query_result, username):
    list = []
    
    # Clear term list of unassigned terms from last search.
    clear_term_list(username)
    
    # If no terms provided, exit process.
    if (termList == []):
        return query_result
    
    # for each query result, get applicable KTOPS and perform analysis
    for record in query_result:
        k_list = KTOPS.objects.filter(fid_id=record.pk)
        list = check_k_list(termList, k_list)
        
        # Insert Title check for word matching
        hold = return_parts_of(termList, [record.title])
        
        # add members of hold to list if not duplicates.
        for i in hold:
            if i not in list:
                list.append(i)
        
        # if no matches, remove record from queryset.
        # if matches exist, keep record and add terms.
        if len(list) == 0:
            query_result = query_result.exclude(pk=record.pk)
        else:
            # save term list to SearchResults
            prep_term_list(record, termList, username)
    
    return query_result

# ------------------------------------------------------------------------------------------------------------------

'''Returns the results of the search parameters.'''
def perform_search(exts, sDate, eDate, wc_min, wc_max, terms, username):
    search_results = []
    
    # Convert string to a list of individual words
    termList = terms.split()
    
    # filter all files by search parameters, returns queryset.
    search_results = query_SourceFiles(exts, sDate, eDate, wc_min, wc_max)
    
    # For filtered queryset, perform term comparison and save search results queryset.
    search_results = term_search(termList, search_results, username)
    
    # save search results to SearchResults
    save_search_result(search_results, username)

