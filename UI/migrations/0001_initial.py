# Generated by Django 5.0.3 on 2024-03-29 13:06

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Aim",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32)),
                ("user_name", models.CharField(max_length=32)),
                ("birthday", models.CharField(max_length=12)),
                ("gender", models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name="Label",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label", models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name="RootBilibili",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label", models.CharField(max_length=64)),
                ("user_name", models.CharField(max_length=32)),
                ("aim_name", models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name="RootBiliT",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_name", models.CharField(max_length=32)),
                ("aim_name", models.CharField(max_length=32)),
                ("label", models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name="RootInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32)),
                ("password", models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name="UserBilibili",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label", models.CharField(max_length=64)),
                ("user_name", models.CharField(max_length=32)),
                ("aim_name", models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name="UserInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32)),
                ("password", models.CharField(max_length=64)),
            ],
        ),
    ]