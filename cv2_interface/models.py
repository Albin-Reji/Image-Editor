from django.db import models

class Images(models.Model):
    name=models.CharField('Image Name', max_length=100)
    upload_image=models.ImageField( upload_to="images/")

    def __str__(self):
        return self.name