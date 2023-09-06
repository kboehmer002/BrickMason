'''======================================== Source Importer ========================================'''
'''
This module contains processes for importing files into the Brick Mason Database and preprocessing
those files for later use in search and new Brick generation.
'''
'''============================================ Includes ==========================================='''

from brick_mason.settings import COMPREHEND, AWS_STORAGE_BUCKET_NAME, REKOGNITION
import docx
from home.models import SourceFile as sf, KTOPS, ContradictionList as cl, RedundantList as rl
from tkinter.messagebox import showinfo
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.filedialog import askopenfile, asksaveasfile
from django.core.files import File
from pathlib import Path
import subprocess
import os
import time
import datetime
import base64

'''================================= Select/Screen Files For Upload ================================='''
'''Process for allowing the user to select one or more files for upload, and performs verification.  '''

# if file tile matches an existing stored file title return true, else false.
def duplicate_file_exists(t):
    if sf.objects.filter(title=t).exists():
        tk.messagebox.showerror(title='Duplicate File',
                                message='A file with the following title already exists in the database: ' + t)
        return True
    return False

#-------------------------------------------------------------------------------------------------------

# Checks if file path exists, path is to a file, and file opens.
def opCheck(f):
    if (not os.path.isfile(f) or not os.path.exists(f)):
        return -1
    try:
        os.path.isfile(f)
        os.path.exists(f)
        f_hold = os.open(f, os.O_WRONLY)
        os.close(f_hold)
        return 1
    except (IOError, OSError, f_hold.DecompressionBombError):
        tk.messagebox.showerror(title='Corrupt File',
                                message='An error occured in attempting to verify the file at: ' + f)
        return -1

# -------------------------------------------------------------------------------------------------------

# use selects one or more files with File Dialog, returns list of paths.
def selectFiles():
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        list = fd.askopenfilenames(
            title="Select a file of any type",
            filetypes=[("All files", "*.*")]
        )
        root.destroy()
        return list

    #second attempt if fail on first attempt, returns 
    except:
        return ""
        
#-------------------------------------------------------------------------------------------------------

#use selects file(s) with File Dialog, file(s) are checked and stored in db.
def addSourceFile(files):
    for i in files:
        path = Path(i)
        
        # seperate Title, check if it exists in database
        file_name = os.path.basename(path)
        t = os.path.splitext(file_name)
        t = t[0]
        if duplicate_file_exists(t):
            continue
        
        # get and save file date modified as date.
        dtm = time.ctime(os.path.getmtime(path))
        dm = datetime.datetime.strptime(dtm, "%c")

        # if file is valid, save file
        if (opCheck(path) == 1):        
            with path.open(mode='rb') as f:
                # *** Add word count
                s_file = sf(file=File(f, name=path.name), title=t,
                            date_modified=dm, word_count=0, preprocessed=0)
                s_file.save()


'''============================================= KTOPS ============================================='''
'''Access KTOPS RDS table for adding, modifying, or removing data.                                  '''

# Stores list of words/phrases in RDS KTOPS table, maintains relationship to image file.
def set_ktops(f_record, ktop_list):
    for ktop in ktop_list:
        obj = KTOPS(fid_id=f_record.pk, ktops=ktop)
        obj.save()

#-------------------------------------------------------------------------------------------------------

# get all ktops for the given file
def get_ktops_by_file(f_record):
    return KTOPS.objects.filter(fid_id=f_record.pk)


'''========================================== SourceFile ==========================================='''
'''Access SourceFile RDS table for adding, modifying, or removing data.                             '''

# find file in SourceFile and set word_count.
def set_word_count(f_record, word_count):
    f_record.word_count = word_count
    f_record.save()

# -------------------------------------------------------------------------------------------------------

# find file in SourceFile and set preprocess to provided state.
def set_preprocessed(f_record, state):
    f_record.preprocessed = state
    f_record.save()
    

'''========================================== Image Files =========================================='''
'''Given a single image file, stores a word list of objects detected in the image, using Rekognition'''

# For the provided file, use AWS Rekognition to generate a list of words
# related to the image and store those with high confidence in KTOPS table.
def set_image_tags(f_record):
    #bucket = get_bucket_name()  # S3 bucket name
    object_list = getObjectList(f_record.file)
    set_ktops(f_record, object_list)

#-------------------------------------------------------------------------------------------------------

# For the image held in this S3 bucket, return list of objects above set confidence.
def getObjectList(image):
    objects = []

    #analyzes images, returns list of labels.
    response = REKOGNITION.detect_labels(Image={'S3Object': {'Bucket': AWS_STORAGE_BUCKET_NAME, 'Name': image.name}},
                                         MaxLabels=10, MinConfidence=80)

    # Get image labels from Rekognition analysis.
    labels = response['Labels']
    
    # Store lebel name if confidence requirement is met.
    for label in labels:
        objects.append(label['Name'])

    # Return the list of words.
    return objects


'''======================================== Word/Text Files ========================================='''
'''Given a single word or text file, returns a word list of objects detected in the image, using Rekognition'''

# Returns extracted text from docx file
def extract_from_docx(word_file):
    doc = docx.Document(word_file)
    text = '\n'.join([p.text for p in doc.paragraphs])
    return text

#-------------------------------------------------------------------------------------------------------

# Returns the number of words in 
def get_text_word_count(text): return len(text.split())

#-------------------------------------------------------------------------------------------------------

# For text provided, AWS Comprehend determines the important phrases, which
# are returned as a list [phrase]
def get_text_key_phrases(rtnd_text):
    keyPhraseSet = []
    k_phrases = COMPREHEND.detect_key_phrases(Text=rtnd_text, LanguageCode='en')
    for phrase in k_phrases['KeyPhrases']:
        keyPhraseSet.append(phrase['Text'])
    return keyPhraseSet

#-------------------------------------------------------------------------------------------------------

# For text provided, AWS Comprehend determines the important entities, which
# are returned as a list [entity] for those above the set level of confidence.
def get_text_entities(rtnd_text):
    entity_set = []
    min_confidence = 80
    entities = COMPREHEND.detect_entities(Text=rtnd_text, LanguageCode='en')
    for entity in entities['Entities']:
        if (entity['Score'] < min_confidence):
                continue
        else:
            entity_set.append(entity['Text'])
    return entity_set

# -------------------------------------------------------------------------------------------------------

# For text provided, AWS Comprehend breaks down sentence structure to
# return sytax of the words for further analysis.
# Tag Values: ADJ | ADP | ADV | AUX | CONJ | CCONJ | DET | INTJ | NOUN | NUM | O
#                 | PART | PRON | PROPN | PUNCT | SCONJ | SYM | VERB
# return syntax 2D list in the form [text][tag]
def get_text_syntax(rtnd_text):
    syntax_set = [[], []]  # row[col]
    min_confidence = 80
    syntax_list = COMPREHEND.detect_syntax(Text=rtnd_text, LanguageCode='en')
    # output sytnax list in form: [[text][pos]]
    for syntax in syntax_list['SyntaxTokens']:
        for pos in syntax['PartOfSpeech']:
            if (pos['Score'] < min_confidence):
                continue
            else:
                syntax_set[0].append(syntax['Text'])
                syntax_set[1].append(pos['Tag'])
    return syntax_set    

# -------------------------------------------------------------------------------------------------------

def text_analysis(f_record):
    rtnd_text = extract_from_docx(f_record.file)
    
    # No text to analyze, exit
    if len(rtnd_text) == 0:
        return
    
    # determine and store file key phrases.
    key_phrases = get_text_key_phrases(rtnd_text)
    set_ktops(f_record, key_phrases)
    
    # determine and store word count of text file.
    word_count = get_text_word_count(rtnd_text)
    set_word_count(f_record, word_count)
    
    # determine and store key words of text file. This appears to be part of key phrases, just use key phrase?
    # key_words = get_keywords(rtnd_text)
    # set_ktops(f_record, key_words)
    
    # determine and store topics of text file. Requires training.
    # topics = get_topics(rtnd_text)
    # set_ktops(f_record, topics)
    
    # determine and store topics of text file. Requires training.
    # entities = get_entities(rtnd_text)
    # set_ktops(f_record, entities)
    
# -------------------------------------------------------------------------------------------------------

def convert_to_sentence_list(f_record_text):
    print("EMPTY convert_to_sentence_list STUB!!!")

# -------------------------------------------------------------------------------------------------------

''' For the pair for sentences, taken from the provided record file, check for
    similar or contradictory sentences.''' 
def sentence_comparator(f_record, comp_f_record, sentence, comp_sentence):
    print("EMPTY sentence_comparator STUB!!!")
    
    # check for redundancies, each sentence against all stored files
    ##if (is_redundant(sentence, comp_sentence)):
    ##set_redundancies(f_record, comp_f_record, sentence, comp_sentence)

    # check for contradications, each sentence against all stored files
    ##if (is_redundant(sentence, comp_sentence)):
    ##set_redundancies(f_record, comp_f_record, sentence, comp_sentence)

'''========================================= Preprocessing =========================================='''

# Goes through each file record not preprocessed and, depending on file type, has the file
# examined and saved.
def preprocess():
    queryset = sf.objects.filter(preprocessed=0)
    if queryset.exists():
        for f_record in queryset:
            
            # if image file, perform analysis.
            if f_record.file.name.endswith(('.png', '.jpg')):
                # Uses Rekognition, c/o outside test/demo
                set_image_tags(f_record)
                set_preprocessed(f_record, 1)
                
            # else if word document, perform analysis.
            elif f_record.file.name.endswith('.docx'):
                # Uses Comprehend, c/o outside test/demo
                text_analysis(f_record)
                set_preprocessed(f_record, 1)
            
                # For each text file to be preprocessed, compare to all
                # other docx files
                ##comp_queryset = queryset.filter(file__icontains='.docx')

                # for each unprocessed record, go through each sentence, compare against all
                # other sentences in all files, not just preprocessed, checking for similar
                # or contradicting sentences.
                ##f_record_text = extract_from_docx(f_record.file)
                ##sentence_list = convert_to_sentence_list(f_record_text)
                
                ##for comp_f_record in comp_queryset:
                    ##comp_f_record_text = extract_from_docx(f_record.file)
                    ##comp_sentence_list = convert_to_sentence_list(f_record_text)

                    ##for sentence in sentence_list:
                        ##for comp_sentence in comp_sentence_list:
                            ##sentence_comparator(f_record, comp_f_record, sentence, comp_sentence)
            
            # else, for unsupported file, inform user.
            else:
                tk.messagebox.showerror(title='Unsupported File',
                                        message='The following unsupported file has been uploaded: ' + f_record.file.name)

            
            
'''============================================== MISC =============================================='''
''' WIP/Extra Functions that currently serve no purpose.                                             '''

# makes window the topmost window.
def raise_above_all(window):
    window.attributes('-topmost', 1)
    window.attributes('-topmost', 0)

# Use file explorer to select a file to open.
def openFile():
   # selecting the file using the askopenfilename() method of filedialog
    file = fd.askopenfilename(
        title="Select a file of any type",
        filetypes=[("All files", "*.*")]
    )
    # cancle / empty handler
    if file is not (None or ''):
        os.startfile(os.path.abspath(file))

# INCOMPLETE: perform antivirus scan via command line on file.
def antivirusScan(f):
    try:
        # need to determine antivirus command line call.
        command_string = 'my_virusscanner -parameters ' + f
        result = subprocess.check_output(
            command_string, stderr=subprocess.STDOUT, shell=True)
        # if needed, do something with "result"
    except subprocess.CalledProcessError as e:
        # if your scanner gives an error code when detecting a virus, you'll end up here
        pass
    except:
        # something else went wrong
        # check sys.exc_info() for info
        pass
