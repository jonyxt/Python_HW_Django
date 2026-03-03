from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


class Phone(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    image = models.URLField()
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
