from django import forms
from .models import HousekeeperRequest

class HousekeeperRequestForm(forms.ModelForm):
    class Meta:
        model = HousekeeperRequest
        fields = ['nationality', 'service_type']
        widgets = {
            'user': forms.HiddenInput(),
            'request_date': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        super().__init__(*args, **kwargs)
        if 'user' in initial:
            self.fields['user'].initial = initial['user']
        if 'request_date' in initial:
            self.fields['request_date'].initial = initial['request_date']
        