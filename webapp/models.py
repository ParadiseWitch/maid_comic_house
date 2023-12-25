from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Comic(models.Model):
    id = models.CharField(primary_key=True)
    url = models.CharField(max_length=1024)
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=2048)
    status = models.CharField(max_length=3)
    start_date = models.DateField()
    last_update_date = models.DateField()

    def __str__(self):
        return self.name


class Chapter(models.Model):
    id = models.AutoField(primary_key=True)
    comic = models.ForeignObjectRel(Comic, on_delete=models.CASCADE)
    url = models.CharField(max_length=1024)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    chapter = models.ForeignObjectRel(Chapter, on_delete=models.CASCADE)
    url = models.CharField(max_length=1024)
    path = models.CharField(max_length=1024)

    def __str__(self):
        return self.url
