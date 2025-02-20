from django.db import models


class Account(models.Model):
    email = models.EmailField(primary_key=True)

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'account'