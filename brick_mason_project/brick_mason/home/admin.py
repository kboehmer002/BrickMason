from django.contrib import admin
from .models import SourceFile, KTOPS, ContradictionList, RedundantList, \
    OutdatedList, ReferenceList, Brick, SearchResult, PermissionChangeRequest, \
    ExtractInsert, TermList

# Register your models here.
admin.site.register(SourceFile)
admin.site.register(KTOPS)
admin.site.register(ContradictionList)
admin.site.register(RedundantList)
admin.site.register(OutdatedList)
admin.site.register(ReferenceList)
admin.site.register(Brick)
admin.site.register(SearchResult)
admin.site.register(PermissionChangeRequest)
admin.site.register(ExtractInsert)
admin.site.register(TermList)