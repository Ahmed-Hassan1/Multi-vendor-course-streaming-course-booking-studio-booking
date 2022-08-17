from django.db import models

# Create your models here.
class OpenDates(models.Model):
    DAY_CHOICES=(
        ('Saturday','Saturday'),
        ('Sunday','Sunday'),
        ('Monday','Monday'),
        ('Tuesday','Tuesday'),
        ('Wednsday','Wednsday'),
        ('Thursday','Thursday'),
        ('Friday','Friday'),
    )

    HOUR_CHOICES=(
        ('0','12 am'),('1','1 am'),('2','2 am'),('3','3 am'),
        ('4','4 am'),('5','5 am'),('6','6 am'),('7','7 am'),
        ('8','8 am'),('9','9 am'),('10','10 am'),('11','11 am'),
        ('12','12 pm'),('13','1 pm'),('14','2 pm'),('15','3 pm'),
        ('16','4 pm'),('17','5 pm'),('18','6 pm'),('19','7 pm'),
        ('20','8 pm'),('21','9 pm'),('22','10 pm'),('23','11 pm'),
    )

    day = models.CharField(max_length=20,choices=DAY_CHOICES)
    start_hour = models.CharField(max_length=20,choices=HOUR_CHOICES,default='12 am')
    end_hour = models.CharField(max_length=20,choices=HOUR_CHOICES,default='11 pm')
    price = models.FloatField(default=100)

    def __str__(self) -> str:
        return self.day+": "+self.get_start_hour_display()+" - "+self.get_end_hour_display()


class Reservations(models.Model):
    HOUR_CHOICES=(
        ('0','12 am'),('1','1 am'),('2','2 am'),('3','3 am'),
        ('4','4 am'),('5','5 am'),('6','6 am'),('7','7 am'),
        ('8','8 am'),('9','9 am'),('10','10 am'),('11','11 am'),
        ('12','12 pm'),('13','1 pm'),('14','2 pm'),('15','3 pm'),
        ('16','4 pm'),('17','5 pm'),('18','6 pm'),('19','7 pm'),
        ('20','8 pm'),('21','9 pm'),('22','10 pm'),('23','11 pm'),
    )
    STATUS_CHOICES=[
        ('Pending','Pending'),
        ('Confirmed','Confirmed'),
        ('Cancelled','Cancelled'),
        ('Completed','Completed'),
        ]
    unique_id=models.IntegerField()
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    day = models.CharField(max_length=20)
    start_hour = models.CharField(max_length=20,choices=HOUR_CHOICES)
    end_hour = models.CharField(max_length=20,choices=HOUR_CHOICES)
    price = models.FloatField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES)

    
    def __str__(self):
        
        #return self.day+": "+HOUR_CHOICES[int(self.start_hour)][1]+" - "+HOUR_CHOICES[int(self.end_hour)][1]
        #return self.day+": "+self.get_start_hour_display()+" - "+self.get_end_hour_display()
        return str(self.unique_id)