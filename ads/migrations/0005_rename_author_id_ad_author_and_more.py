# Generated by Django 4.1.4 on 2023-01-15 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ads", "0004_alter_category_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="ad",
            old_name="author_id",
            new_name="author",
        ),
        migrations.RenameField(
            model_name="ad",
            old_name="category_id",
            new_name="category",
        ),
        migrations.RemoveField(
            model_name="user",
            name="location_id",
        ),
        migrations.AddField(
            model_name="user",
            name="location",
            field=models.ManyToManyField(to="ads.location"),
        ),
        migrations.AlterField(
            model_name="ad",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
        migrations.AlterField(
            model_name="location",
            name="lat",
            field=models.DecimalField(
                blank=True, decimal_places=6, max_digits=8, null=True
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="lng",
            field=models.DecimalField(
                blank=True, decimal_places=6, max_digits=8, null=True
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="name",
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="age",
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("member", "Пользователь"),
                    ("moderator", "Модератор"),
                    ("admin", "Администратор"),
                ],
                default="member",
                max_length=9,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(default="", max_length=20, unique=True),
        ),
    ]
