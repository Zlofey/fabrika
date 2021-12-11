from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils import timezone

from core.models import Poll


class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.pk:
            start_date = self.instance.start_date
        else:
            start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date >= end_date:
            raise ValidationError('Start date later or equal than end date.')
        return cleaned_data

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        now = timezone.now()
        if start_date < now:
            self.add_error('start_date', 'Start date earlier than now.')
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        now = timezone.now()
        if end_date < now:
            self.add_error('end_date', 'End date earlier than now.')
        return end_date
