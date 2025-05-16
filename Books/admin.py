from django.contrib import admin
from .models import Subject, Author, BookDetail, BookIssueApproval, RecentAct
# Register your models here.


admin.site.register(Subject)
admin.site.register(Author)
admin.site.register(BookDetail)
admin.site.register(BookIssueApproval)
admin.site.register(RecentAct)