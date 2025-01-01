from django.forms import ModelForm

from .models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        # Include only specific fields
        fields = ['name', 'topic', 'description']

        # Customize widgets

        # Add labels (optional)
        labels = {
            'name': 'Room Name',
            'topic': 'Topic',
            'description': 'Description',
        }

