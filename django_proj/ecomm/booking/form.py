from django import forms
from .models import OpenDates


class OpenDateForm(forms.ModelForm):
    class Meta:
        model = OpenDates
        fields = '__all__'

    def clean(self):
        start = self.cleaned_data['start_hour']
        end = self.cleaned_data['end_hour']


        current_day= OpenDates.objects.all()
        days_list=[]
        for entry in current_day:
            days_list.append(entry.day)
        
        if self.cleaned_data['day'] in days_list:
            raise forms.ValidationError("Day already exists")

        if int(end) <= int(start):
            raise forms.ValidationError('Choose an End hour after the start hour')
        
        return self.cleaned_data
        