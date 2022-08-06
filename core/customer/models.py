from django.db import models

# Create your models here.
class Customer(models.Model):
    """Customer Info"""

    name = models.CharField(max_length=250, blank=True, null=True)
    surname = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Passport(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, blank=True, null=True
    )
    scan_file = models.ImageField(upload_to="passport/", blank=True, null=True)
    document_number = models.CharField(max_length=250, blank=True, null=True)
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    patronymic = models.CharField(max_length=250, blank=True, null=True)
    nationality = models.CharField(max_length=250, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    personal_number = models.CharField(max_length=250, blank=True, null=True)
    gender = models.CharField(max_length=250, blank=True, null=True)
    issue_date = models.DateField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    issuing_authority = models.CharField(max_length=250, blank=True, null=True)
