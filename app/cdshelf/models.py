from django.db import models


class SourceDir(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=500)

    def __str__(self):
        return self.location


class Artist(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Cd(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Song(models.Model):
    title = models.CharField(max_length=200)
    track = models.IntegerField()
    cd = models.ForeignKey(Cd, on_delete=models.CASCADE)
    filepath = models.CharField(max_length=500)

    def __str__(self):
        return self.title
