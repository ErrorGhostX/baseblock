from django import forms
from .models import Event

class EventAttendanceForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['participants']
        widgets = {
            'participants': forms.CheckboxSelectMultiple(),  # Множественный выбор
        }

from django import forms
from .models import Event

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
            'title': forms.TextInput(attrs={
                'class': 'bg-gray-700 text-white border border-gray-600 rounded-lg p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-600',
                'placeholder': 'Введите название ивента',
            }),
            'description': forms.Textarea(attrs={
                'class': 'bg-gray-700 text-white border border-gray-600 rounded-lg p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-600',
                'rows': 4,
                'placeholder': 'Введите описание ивента и его правила',
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'bg-gray-700 text-white border border-gray-600 rounded-lg p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-600',
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'bg-gray-700 text-white border border-gray-600 rounded-lg p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-600',
            }),
            'location': forms.TextInput(attrs={
                'class': 'bg-gray-700 text-white border border-gray-600 rounded-lg p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-600',
                'placeholder': 'Введите место проведения',
            }),
            'coordinates': forms.TextInput(attrs={
                'class': 'bg-gray-700 text-white border border-gray-600 rounded-lg p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-600',
                'placeholder': 'Введите координаты (необязательно)',
            }),
            'image1': forms.ClearableFileInput(attrs={
                'class': 'bg-gray-700 text-white border border-gray-600 rounded-lg p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-600',
            }),
            'image2': forms.ClearableFileInput(attrs={
                'class': 'bg-gray-700 text-white border border-gray-600 rounded-lg p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-600',
            }),
            'image3': forms.ClearableFileInput(attrs={
                'class': 'bg-gray-700 text-white border border-gray-600 rounded-lg p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-600',
            }),
        }
