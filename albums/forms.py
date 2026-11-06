from django import forms

class AlbumForm(forms.Form):
    title = forms.CharField(label="Название альбома", max_length=200)
    artist = forms.CharField(label="Исполнитель", max_length=200)
    year = forms.IntegerField(label="Год выпуска", min_value=1900, max_value=2026)
    genre = forms.CharField(label="Жанр", max_length=100)
    tracks = forms.IntegerField(label="Количество треков", min_value=1)