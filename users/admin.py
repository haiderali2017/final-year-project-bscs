from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.timezone import now

from .forms import ApplicantCreationForm, ApplicantChangeForm
from .models import *
from django.contrib import admin


def make_company(modeladmin, request, queryset):
    queryset.update(is_company=True)

make_company.short_description = "Mark selected Jobs as Companies"


def make_applicant(modeladmin, request, queryset):
    queryset.update(is_company=False)

make_applicant.short_description = "Mark selected Jobs as Applicants"


class ApplicantAdmin(UserAdmin):
    model = Applicant
    actions = [make_company, make_applicant]
    list_display = ['username', 'email', 'is_company', 'password', ]


def make_published(modeladmin, request, queryset):
    queryset.update(status=True, posted_at=now())

make_published.short_description = "Mark selected Jobs as published"


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['Job_title', 'status', 'posted_by']
    ordering = ['Job_title', 'posted_at']
    actions = [make_published]

admin.site.register(Job_Post, ArticleAdmin)



admin.site.register(Applicant, ApplicantAdmin)
# admin.site.register(Company, CompanyAdmin)

admin.site.register(Document)
admin.site.register(company_profile)
admin.site.register(AppliedJobs)
admin.site.register(Resume)
admin.site.register(Resume_Education)
admin.site.register(Resume_Skills)
