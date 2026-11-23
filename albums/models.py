from django.db import models

class Album(models.Model):
    title = models.CharField("Название альбома", max_length=200)
    artist = models.CharField("Исполнитель", max_length=200)
    year = models.IntegerField("Год выпуска")
    genre = models.CharField("Жанр", max_length=100)
    tracks = models.IntegerField("Количество треков")
    record_label = models.CharField("Лейбл", max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"
        unique_together = ('title', 'artist') 

    def __str__(self):
        return f"{self.title} - {self.artist}"