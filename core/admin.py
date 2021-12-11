from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedTabularInline
from core.forms import PollForm
from core.models import *


class AnswerInline(NestedTabularInline):
    model = Answer
    fields = ['text']

    def get_extra(self, request, obj: Question = None, **kwargs):
        if obj and obj.type == Question.TYPE_TEXT:
            return 0
        return 1


class QuestionInline(NestedTabularInline):
    model = Question
    extra = 1
    inlines = [AnswerInline]
    fields = ['type', 'text']


@admin.register(Poll)
class PollAdmin(NestedModelAdmin):
    list_display = [
        'id',
        'name',
        'start_date',
        'end_date',
    ]
    inlines = [QuestionInline]
    form = PollForm

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if obj:
            fields.append('start_date')
        return fields
