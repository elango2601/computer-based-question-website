from django import forms
from .models import Question

class QuestionAdminForm(forms.ModelForm):
    options_csv = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Enter options separated by comma (e.g. Option A, Option B). Default is JSON list."
    )

    class Meta:
        model = Question
        fields = '__all__'
        exclude = ('options',) # We handle options via options_csv
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Populate options_csv from JSON options
            opts = self.instance.options
            if isinstance(opts, list):
                self.initial['options_csv'] = ', '.join(opts)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        csv = self.cleaned_data.get('options_csv', '')
        if csv:
             instance.options = [x.strip() for x in csv.split(',') if x.strip()]
        else:
             instance.options = []
        if commit:
            instance.save()
        return instance
