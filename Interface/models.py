from django.db import models


class NavTop(models.Model):

    nome = models.CharField(
        max_length=100
    )

    url = models.CharField(
        max_length=200
    )

    def __str__(self):
        return self.nome


class MenuItem(models.Model):

    nome = models.CharField(
        max_length=100
    )

    icone = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nome


class SubMenuItem(models.Model):

    menu = models.ForeignKey(
        MenuItem,
        related_name="subitens",
        on_delete=models.CASCADE
    )

    nome = models.CharField(
        max_length=100
    )

    url = models.CharField(
        max_length=255,
        blank=True
    )

    def __str__(self):
        return self.nome


class SubSubMenuItem(models.Model):

    submenu = models.ForeignKey(
        SubMenuItem,
        related_name="subitens",
        on_delete=models.CASCADE
    )

    nome = models.CharField(
        max_length=100
    )

    url = models.CharField(
        max_length=255
    )

    def __str__(self):
        return self.nome