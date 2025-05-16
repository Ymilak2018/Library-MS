from django.db import models
from datetime import datetime
from django.utils import timezone


# Create your models here.
class Subject(models.Model):
    sub = models.CharField(max_length=50, verbose_name='Subject Name', unique=True)

    def __str__(self):
        return self.sub

class Author(models.Model):
    sub = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Subject Name')
    name = models.CharField(max_length=50, verbose_name='Author\'s Name', unique=True)
    def __str__(self):
        return self.name

class BookDetail(models.Model):
    sub = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Subject Name')
    title = models.CharField(verbose_name='Title of the Book', max_length=50, null=True)
    author = models.ManyToManyField(Author)
    pub = models.CharField(verbose_name='Publsiher\'s Name', max_length=50, null=True)
    avail = models.BooleanField(verbose_name='Availability', null=True)
    coverp = models.ImageField(verbose_name='Cover Page', upload_to='cover_pages/')

    def __str__(self):
        return f"{self.title} by { ',' . join([author.name for author in self.author.all()])} - ({self.sub})"



class BookIssueApproval(models.Model):
    bookn = models.CharField(verbose_name='Book Name', max_length=50)
    sub = models.CharField(verbose_name='Subject', max_length=50, default='Null')
    coverp = models.ImageField(verbose_name='Cover Page', upload_to='cover_pages/', default='-')
    isstime = models.DateField(verbose_name='Date of the Issue', max_length=50)
    issuer = models.CharField(verbose_name='Issuer Name', max_length=50)
    approve = models.CharField(verbose_name='Approval Status', choices=(('Approve', 'Approve'), ('Decline', 'Decline'), ('Not viewed', "Not viewed")), default='Not viewed', max_length=50)

    def __str__(self):
        return f"{self.bookn} -- issued by -- {self.issuer}"



class RecentAct(models.Model):
    cat = models.CharField(verbose_name='Category', choices=(
            ("user_borrow_book", "User Borrow Book"),
            ("user_return_book", "User Return Book"),
            ("new_user_registered", "New User Registered"),
            ("new_book_added", "New Book Added"),
            ("new_author_registered", "New Author Registered"),
            ("new_subject_added", "New Subject Added")
    ), max_length=50)
    content = models.TextField(verbose_name='Activity')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.get_cat_display()} -- {self.id}"
