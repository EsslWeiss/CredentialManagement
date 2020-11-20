from django.db import models


class Customer(models.Model):
    first_name = models.CharField('first name', max_length=75)
    last_name = models.CharField('last name', max_length=75)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=120)
    description = models.TextField()
    createdAt = models.DateTimeField('created at', auto_now_add=True)

    def __str__(self):
        return '({}) {} {}'.format(self.email, self.first_name, self.last_name)

