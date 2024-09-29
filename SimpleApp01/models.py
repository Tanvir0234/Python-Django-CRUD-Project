from django.db import models

# Create your models here.
class Trainee(models.Model):
    TraineeID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=30)
    ContactNo = models.CharField(max_length=15)
    ContactAddress = models.CharField(max_length=100)
    EmailAddress = models.EmailField()  
    BatchNo = models.CharField(max_length=30 , default="N\A")

    class Meta:
        db_table="Trainee"