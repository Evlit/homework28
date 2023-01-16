from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)
    lat = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True )
    lng = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Расположение'
        verbose_name_plural = 'Расположения'


class User(models.Model):
    ROLE = [
        ("member", "Пользователь"),
        ("moderator", "Модератор"),
        ("admin", "Администратор"),
    ]
    first_name = models.CharField(max_length=20, default='')
    last_name = models.CharField(max_length=20, default='')
    username = models.CharField(max_length=20, default='', unique=True)
    password = models.CharField(max_length=20, default='123')
    role = models.CharField(max_length=9, default='member', choices=ROLE)
    age = models.PositiveSmallIntegerField(default=0)
    location = models.ManyToManyField(Location)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ["username"]


class Category(models.Model):
    name = models.CharField(max_length=100, default='', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Ad(models.Model):
    name = models.CharField(max_length=200, default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    description = models.TextField(default='')
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
