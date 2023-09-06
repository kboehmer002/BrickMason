from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
#from safe_filefield.models import SafeFileField
import os

# Storage Database Table for Source Files. Users save files here for
# use in drafting bricks.
class SourceFile(models.Model):
    file = models.FileField()
    title = models.CharField(max_length=100)
    date_modified = models.DateField()
    word_count = models.IntegerField(default=0)
    preprocessed = models.BooleanField(default=False)
    #file = SafeFileField(scane_viruses=True)

# --------- receiver action ---------

# Deletes file on deletion from S3 db.
@receiver(pre_delete, sender=SourceFile)
def SourceFile_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)

# --------- receiver action ---------

# Deletes old file and replaces with new one when replaced in S3 db.
@receiver(pre_save, sender=SourceFile)
def SourceFile_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = SourceFile.objects.get(pk=instance.pk).file
    except SourceFile.DoesNotExist:
        return False
    
    new_file = instance.file
    if not old_file == new_file:
        old_file.delete(False)

# ----------------------------------------------------------------------------------------------------------------

# Key words, topics, objects, and phrases list for each file.
# Deletion controled by existance of related source file (fid).
class KTOPS(models.Model):
    fid = models.ForeignKey("SourceFile", on_delete=models.CASCADE)
    ktops = models.CharField(max_length=150)

# ----------------------------------------------------------------------------------------------------------------

# A list of sentence pairs that have been determined to be in
# contradiction with each other. Deletion controled by existance
# of related source file (fid).
class ContradictionList(models.Model):
    fid = models.ForeignKey("SourceFile", on_delete=models.CASCADE)
    pid = models.BigIntegerField()
    sentence = models.CharField(max_length=150)

# ----------------------------------------------------------------------------------------------------------------

# A list of sentence pairs that have been determined to be
# redundant with each other. Deletion controled by existance of
# related source file (fid).
class RedundantList(models.Model):
    fid = models.ForeignKey("SourceFile", on_delete=models.CASCADE)
    pid = models.BigIntegerField()
    sentence = models.CharField(max_length=150)

# ----------------------------------------------------------------------------------------------------------------

# A list of sentences that have been determined to be outdated by a
# user. Deletion controled by existance of related source file (fid).
class OutdatedList(models.Model):
    fid = models.ForeignKey("SourceFile", on_delete=models.CASCADE)
    pid = models.BigIntegerField()
    sentence = models.CharField(max_length=150)

# ----------------------------------------------------------------------------------------------------------------

# A list of references that have been used to create a brick. Used
# to hold working set documents and delete if correcsponding Brick
# (bid) has been deleted. 
class ReferenceList(models.Model):
    bid = models.ForeignKey("Brick", on_delete=models.CASCADE)
    fid = models.ForeignKey("SourceFile", on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='workfile', null=True)

# --------- receiver action ---------

# Deletes file on deletion from S3 db.
@receiver(pre_delete, sender=ReferenceList)
def ReferenceList_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)

# --------- receiver action ---------

# Deletes old file and replaces with new one when replaced in S3 db.
@receiver(pre_save, sender=ReferenceList)
def ReferenceList_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = ReferenceList.objects.get(pk=instance.pk).file
    except ReferenceList.DoesNotExist:
        return False
    
    new_file = instance.file
    if not old_file == new_file:
        old_file.delete(False)
        
# ----------------------------------------------------------------------------------------------------------------

# A list of Bricks that have been made, their current stage, and
# their workspace location.
class Brick(models.Model):
    file = models.FileField(default=None)
    uid = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    stage = models.IntegerField(default=1)
    workspace = models.CharField(max_length=265, default=None)

# --------- receiver action ---------

# Deletes file on deletion from S3 db.
@receiver(pre_delete, sender=Brick)
def Brick_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)

# --------- receiver action ---------

# Deletes old file and replaces with new one when replaced in S3 db.
@receiver(pre_save, sender=Brick)
def Brick_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Brick.objects.get(pk=instance.pk).file
    except Brick.DoesNotExist:
        return False
    
    new_file = instance.file
    if not old_file == new_file:
        old_file.delete(False)
        
# ----------------------------------------------------------------------------------------------------------------

# Temp storage for search results lists, by username. Deletion
# controled by existance of related source file (fid).
class SearchResult(models.Model):
    username = models.CharField(max_length=150)
    fid = models.ForeignKey("SourceFile", on_delete=models.CASCADE)

# ----------------------------------------------------------------------------------------------------------------

# Stores username as uid (user ID) and a comma seperated list of
# groups requested.
class PermissionChangeRequest(models.Model):
    username = models.CharField(max_length=100)
    groups = models.CharField(max_length=100)

# ----------------------------------------------------------------------------------------------------------------

# used as temporary storage by job ID to hold text for analysis. 
class ExtractInsert(models.Model):
    jid = models.IntegerField()
    text = models.TextField()

# ----------------------------------------------------------------------------------------------------------------

# Storage for search terms, by username. Used by editor to
# relate the draft brick to term data organized by reference.
class TermList(models.Model):
    rid = models.ForeignKey("SourceFile", on_delete=models.SET_NULL, null=True)
    bid = models.ForeignKey("Brick", on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=150)
    term = models.CharField(max_length=100)
    word_count = models.IntegerField()
