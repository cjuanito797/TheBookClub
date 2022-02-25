import random

from django.db import models
from accounts.models import User
# Create your models here.

def create_ref_number():
    return str(random.randint(100000, 999999))

class Order(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=6,
        blank=True,
        editable=False,
        unique=True,
        db_index=True,
        default=create_ref_number()
    )

    user = models.ForeignKey(User,
                             related_name='user',
                             on_delete=models.CASCADE,
                             default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created')
        unique_together = (("user", "id", "created"))

    def __str__(self):
        return f'{self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


