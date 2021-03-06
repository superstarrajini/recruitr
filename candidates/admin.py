from coding_problems.models import CodeSubmission
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from recruitr.admin import admin_site
from .models import Candidate


class CodeSubmissionInline(admin.StackedInline):
    model = CodeSubmission
    readonly_fields = ('problem', 'language', 'code', 'error_output',)
    ordering = ('-submission_time',)

    def has_add_permission(self, obj):
        return False

    class Media:
        css = {
            "all": ("css/admin/codesubmission.css",)
        }


class CandidateInline(admin.StackedInline):
    model = Candidate


class ExtendedUserAdmin(UserAdmin):
    list_display = list(UserAdmin.list_display) + ['get_level', 'get_status']
    list_filter = ['is_staff', 'candidate__status', 'candidate__level']
    inlines = [CandidateInline, CodeSubmissionInline]

    def get_level(self, obj):
        return obj.candidate.level
    get_level.admin_order_field = 'level'
    get_level.short_description = 'Candidate level'

    def get_status(self, obj):
        return obj.candidate.status
    get_status.admin_order_field = 'status'
    get_status.short_description = 'Candidate status'


admin_site.register(User, ExtendedUserAdmin)
