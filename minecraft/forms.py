from django import forms
from .models import Event

class EventAttendanceForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['participants']
        widgets = {
            'participants': forms.CheckboxSelectMultiple(),  # Множественный выбор
        }

class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'date',
            'time',
            'location',
            'coordinates',
            'image1',
            'image2',
            'image3',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
