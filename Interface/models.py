from django.db import models

# Create your models here.


class MenuItem(models.Model):
    nome = models.CharField(max_length=100)
    icone = models.CharField(max_length=50, blank=True, null=True)

class SubMenuItem(models.Model):
    menu = models.ForeignKey(MenuItem, related_name='subitens', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    

class NavTop(models.Model):
    nome = models.CharField(max_length=100)
    url = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nome}"