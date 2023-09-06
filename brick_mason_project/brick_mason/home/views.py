from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserUpdateForm, SearchForm
from django.contrib.auth.decorators import login_required
from home.modules import SourceImporter, ContentAnalyzer, ContentGenerator, BricksCreator
from django.contrib.auth.models import Group
from urllib.parse import urlencode

""" Registration page, user to allow new users to register an account.      """
def register(request):
    # upon form submission event, verify inputs are valid
    # and save registration info, and redirect to login.
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            
            #set user's group to brick drafter
            my_group = Group.objects.get(name='Brick Drafter')
            uid = form.instance
            my_group.user_set.add(uid)

            messages.success(
                request, f'Your account has been created. You can log in now!')
            return redirect('login')
        
    # No form submission event
    else:
        form = UserRegistrationForm()

    # Set template variable
    context = {'form': form}
    
    return render(request, 'users/register.html', context)

# ----------------------------------------------------------------------------------------------------------------

""" Dashboard Page provides access to user's bricks, and bricks pending review. """
@login_required #<-- Needed to make log in req'd for following view
def dashboard(request):
    brick_list = ContentAnalyzer.get_user_bricks(request.user.username)
    SME_list = ContentAnalyzer.get_SME_bricks(request.user.username)
    Editor_list = ContentAnalyzer.get_Editor_bricks(request.user.username)
    
    if request.method == 'POST':
        action = request.POST.get("dtitle")
        if not (action is None):
            path = BricksCreator.get_record_path(brick_list, action)
            BricksCreator.open_file(path)
            pass_file = urlencode({'file': path})
            url = '{}?{}'.format('../brick_editor/', pass_file)
            return redirect(url)
        
        action = request.POST.get("stitle")
        if not (action is None):
            path = BricksCreator.get_record_path(brick_list, action)
            BricksCreator.open_file(path)
            pass_file = urlencode({'file': path})
            url = '{}?{}'.format('../brick_editor/', pass_file)
            return redirect(url)
        
        action = request.POST.get("etitle")
        if not (action is None):
            path = BricksCreator.get_record_path(brick_list, action)
            BricksCreator.open_file(path)
            pass_file = urlencode({'file': path})
            url = '{}?{}'.format('../brick_editor/', pass_file)
            return redirect(url)
    
    context = {
        'b_list': brick_list,
        's_list': SME_list,
        'e_list': Editor_list,
    }
    return render(request, 'dashboard.html', context)

# ----------------------------------------------------------------------------------------------------------------

""" Search Page allows user to set parameters and provide terms. Finds files containing subject matter. """
@login_required
def search(request):
    if request.method == 'POST':
        s_form = SearchForm(request.POST)
        if s_form.is_valid():
            exts = s_form.cleaned_data.get("extensions")
            termList = s_form.cleaned_data.get("terms")
            sDate = s_form.cleaned_data.get("sDateModified")
            eDate = s_form.cleaned_data.get("eDateModified")
            wc_min = s_form.cleaned_data.get("wordCountMin")
            wc_max = s_form.cleaned_data.get("wordCountMax")
            ContentAnalyzer.perform_search(
                exts, sDate, eDate, wc_min, wc_max, termList, request.user.username)
            return redirect('search_results/')
    else:
        s_form = SearchForm()
    context = {
        's_form': s_form,
    }
    return render(request, 'search.html', context)

# ----------------------------------------------------------------------------------------------------------------

""" Search Results displays files containing subject matter, for user selection in making bricks. """
@login_required
def search_results(request):
    # get serach result queryset
    queryset = ContentAnalyzer.get_search_result(request.user.username)
    
    # initial ordering state none
    state = ""
    
    # Prepare list for display
    display_list = ContentAnalyzer.get_display_list(queryset)
    
    if request.method == 'POST':
        
        # cancel buttton
        action = request.POST.get("Return to Search")
        if not (action is None):
            return redirect('../search/')
        
        action = request.POST.get("rbutton")
        if not (action is None):
            display_list = ContentAnalyzer.remove_from_list(
                display_list, action, request.user.username)
        
        #action = request.POST.get("opendocx")
        #if not (action is None):
        #    pass_file = urlencode({'file': action})
        #    url = '{}?{}'.format('../../viewdocx/', pass_file)
        #    return redirect(url)
        
        # if action from tbutton, order by title.                
        action = request.POST.get("tbutton")
        if not (action is None):
            state = action
            display_list = ContentAnalyzer.toggle_order_title(
                display_list, state)
        
        # if action from dbutton, order by date modified.
        action = request.POST.get("dbutton")
        if not (action is None):
            state = action
            display_list = ContentAnalyzer.toggle_order_date_modified(
                display_list, state)
            
        # if action from wbutton, order by word count.
        action = request.POST.get("wbutton")
        if not (action is None):
            state = action
            display_list = ContentAnalyzer.toggle_order_word_count(
                display_list, state)
        
        # if action from submit, start new brick generation process.
        action = request.POST.get("submit")
        if not (action is None):
            file = BricksCreator.new_brick_generation(queryset, request.user.username)
            if file != "":
                pass_file = urlencode({'file': file})
                url = '{}?{}'.format('../../brick_editor/', pass_file)
                return redirect(url)
    
    # set template variable.
    context = {
        'results': display_list,
        'state': state,
        'queryset': queryset
    }
    
    return render(request, 'search_results.html', context)

# ----------------------------------------------------------------------------------------------------------------

""" Brick Editor connects tools, db, and word document, to aid in drafting Bricks. """
@login_required
def brick_editor(request):
    path = request.GET.get('file')
    
    if request.method == 'POST':
        action = request.POST.get("selector")
        
        # 0: New Project
        if (action == '0'):
            #BricksCreator.exit_process(path)
            return redirect('../search/')
        
        # 1: Save
        if (action == '1'):
            if (path == "") or (path is None) or (path == "None"):
                BricksCreator.no_brick_loaded()
            else:
                BricksCreator.brick_save(path)
            
        # 2: Save As
        if (action == '2'):
            BricksCreator.brick_save_as(path)
            
        # 3: Load
        if (action == '3'):
            path = BricksCreator.brick_load(path)
            pass_file = urlencode({'file': path})
            url = '{}?{}'.format('.', pass_file)
            return redirect(url)
        
        # 4: Import
        if (action == '4'):
            BricksCreator.import_brick(path)
            
        # 5: Export
        if (action == '5'):
            BricksCreator.export_brick(path)
            
        # 6: Rename
        if (action == '6'):
            if (path == "") or (path is None) or (path == "None"):
                BricksCreator.no_brick_loaded()
            else:                
                path = BricksCreator.rename_brick(path)
                pass_file = urlencode({'file': path})
                url = '{}?{}'.format('.', pass_file)
                return redirect(url)
            
        # 7: Exit
        if (action == '7'):
            #BricksCreator.exit_process(path)
            return redirect('../dashboard/')
        
        # 8: Summarizer
        if (action == '8'):
            if (path == "") or (path is None) or (path == "None"):
                BricksCreator.no_brick_loaded()
            else:
                BricksCreator.summarizer(path)
            
        # 9: Q&A List
        if (action == '9'):
            if (path == "") or (path is None) or (path == "None"):
                BricksCreator.no_brick_loaded()
            else:
                BricksCreator.qa_list(path)
            
        # 10: Image
        if (action == '10'):
            if (path == "") or (path is None) or (path == "None"):
                BricksCreator.no_brick_loaded()
            else:
                BricksCreator.image(path)
            
        # 11: Source Link
        if (action == '11'):
            BricksCreator.source_link(path)
            
        # 12: References
        if (action == '12'):
            BricksCreator.references(path)
            
        # 13: Contradictions
        if (action == '13'):
            BricksCreator.contradictions(path)
            
        # 14: Redundancies
        if (action == '14'):
            BricksCreator.redundancies(path)
            
        # 15: Outdated
        if (action == '15'):
            BricksCreator.outdated(path)
            
        # 16: Side-By-Side
        if (action == '16'):
            BricksCreator.side_by_side(path)
            
        # 17: Popout Reference
        if (action == '17'):
            BricksCreator.popout_reference(path)
            
        # 18: Flag
        if (action == '18'):
            if (path == "") or (path is None) or (path == "None"):
                BricksCreator.no_brick_loaded()
            else:
                BricksCreator.flag(path)
    
        # 19: Set Workspace
        if (action == '19'):
            BricksCreator.set_workspace()

        # 20: Set Stage
        if (action == '20'):
            if (path == "") or (path is None) or (path == "None"):
                BricksCreator.no_brick_loaded()
            else:
                BricksCreator.set_stage(path)
    
    # set template variable.
    context = {
        'path': path
    }
                
    return render(request, 'brick_editor.html', context)

# ----------------------------------------------------------------------------------------------------------------

""" Profile allows user to look, and edit, at their registered information. """
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form,
    }
    return render(request, 'profile.html', context)

# ----------------------------------------------------------------------------------------------------------------

""" ImportNewSource is a back end function call used for selection and preprocessing files. """
@login_required
def ImportNewSource(request):
    SourceImporter.addSourceFile(SourceImporter.selectFiles())
    SourceImporter.preprocess()
    return HttpResponseRedirect('../dashboard/')

# ----------------------------------------------------------------------------------------------------------------

#@login_required
#def viewdocx(request):
#    s3_path = request.GET.get('file')
#    path = 'http://docs.google.com/gview?url=' + s3_path + '&embedded=true'
#    context = {
#        'path': path,
#    }
#    return render(request, 'viewdocx.html', context)
