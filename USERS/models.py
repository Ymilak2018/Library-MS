from django.contrib.auth.models import User
from django.db import models
from Books.models import BookDetail, Subject, Author

from datetime import datetime, timedelta


# Create your models here.


def get_deadline():
    return datetime.today() + timedelta(days=15)



class Borrower(models.Model):

    bwr = models.CharField(verbose_name='User', default='-',max_length=50)
    book = models.CharField(verbose_name='Book Name', max_length=50)
    sub = models.CharField(verbose_name='Subject', max_length=50, default = 'Null')
    img = models.ImageField(verbose_name='Cover Page', upload_to='cover_pages/', default='-')
    bdate = models.DateField(default=datetime.today, verbose_name='Borrowing Date')
    rdate = models.DateField(default=get_deadline(), verbose_name='Returning Date')
    status = models.CharField(verbose_name='Return Status', choices=(('Due', 'Due'), ('Returned', 'Returned'), ('Not Returned', 'Not Returned')), default="Not Returned", max_length=50, null=True)




    def __str__(self):
        return f"{self.bwr}-{self.book}-{self.bdate}"


class Profile(models.Model):
    choices = (
        ('Staff', 'Staff'),
        ('Faculty', 'Faculty'),
        ('Student', 'Student')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, verbose_name='Role', choices=choices)
    libid = models.CharField(max_length=10, verbose_name='LibraryID', unique=True)

    def __str__(self):
        return f"{self.user.username} Profile"