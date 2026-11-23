from django import forms
from .models import Album

class AlbumForm(forms.Form):
     STORAGE_CHOICES = [
        ('file', 'Сохранить в JSON-файл'),
        ('db', 'Сохранить в Базу Данных (SQLite)'),
    ]
     storage_type = forms.ChoiceField(choices=STORAGE_CHOICES, label="Куда сохранить?", widget=forms.RadioSelect)
     title = forms.CharField(label="Название альбома", max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
     artist = forms.CharField(label="Исполнитель", max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
     year = forms.IntegerField(label="Год выпуска", min_value=1900, max_value=2026, widget=forms.NumberInput(attrs={'class': 'form-control'}))
     genre = forms.CharField(label="Жанр", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
     tracks = forms.IntegerField(label="Количество треков", min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
     country = forms.CharField(label="Страна", max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))