from django.db import models


class Comic(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=1024)
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=2048)
    status = models.CharField(max_length=3)
    start_date = models.DateField()
    last_update_date = models.DateField()

    class Meta:
        db_table = 'comic'

    def __str__(self):
        return self.name


class Chapter(models.Model):
    id = models.AutoField(primary_key=True)
    comic_id = models.ForeignObjectRel(to=Comic, field=Comic.id, on_delete=models.CASCADE, )
    url = models.CharField(max_length=1024)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'chapter'

    def __str__(self):
        return self.name


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    chapter_id = models.ForeignObjectRel(to=Chapter, field=Chapter.id, on_delete=models.CASCADE, )
    url = models.CharField(max_length=1024)
    path = models.CharField(max_length=1024)

    class Meta:
        db_table = 'image'

    def __str__(self):
        return self.url


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.name


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'author'

    def __str__(self):
        return self.name


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.name


class ComicAuthor(models.Model):
    id = models.AutoField(primary_key=True)
    comic_id = models.ForeignObjectRel(to=Comic, field=Comic.id, on_delete=models.CASCADE)
    author_id = models.ForeignObjectRel(to=Author, field=Author.id, on_delete=models.CASCADE)

    class Meta:
        db_table = 'comic_author'


class ComicTag(models.Model):
    id = models.AutoField(primary_key=True)
    comic_id = models.ForeignObjectRel(to=Comic, field=Comic.id, on_delete=models.CASCADE)
    Tag_id = models.ForeignObjectRel(to=Tag, field=Tag.id, on_delete=models.CASCADE)

    class Meta:
        db_table = 'comic_tag'
