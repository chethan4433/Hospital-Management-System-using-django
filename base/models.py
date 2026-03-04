from django.db import models

# Create your models here.

class Hospital(models.Model):
    patient = models.CharField(max_length=50)
    doctor = models.CharField(max_length=50)
    disease = models.TextField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phno = models.IntegerField()
    report = models.FileField(upload_to='reports/', null=True, blank=True)


    def __str__(self):
        return self.patient
