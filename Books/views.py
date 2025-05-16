from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm, SubForm, AuthForm
from .models import Subject, Author, BookDetail, BookIssueApproval, RecentAct
from USERS.models import Borrower
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
# Create your views here.
def addbook(request):
    if request.user.is_authenticated and request.user.is_superuser:
        form = BookForm()
        if request.method == 'POST':
            form = BookForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('viewbooks')


            rc = RecentAct.objects.create(cat = "new_book_added", content = f"New Book Added: {form.cleaned_data.get('title')}")
            rc.save()

        return render(request, 'home/addbook.html', {'form': form})

    else:
        messages.info(request, 'Enter the Admin Credentials to view Admin Panel!')
        return redirect('signin')


def addsub(request):
    if request.user.is_authenticated and request.user.is_superuser:
        form = SubForm()
        if request.method == 'POST':
            form = SubForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('viewsub')

            rc = RecentAct.objects.create(cat="new_subject_added", content=f"New Subject Added: {form.cleaned_data.get('sub')}")
            rc.save()

        return render(request, 'home/addsub.html', {'form': form})

    else:
        messages.info(request, 'Enter the Admin Credentials to view Admin Panel!')
        return redirect('signin')


def addauth(request):
    if request.user.is_authenticated and request.user.is_superuser:
        form = AuthForm()
        if request.method == 'POST':
            form = AuthForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('viewauth')

            rc = RecentAct.objects.create(cat="new_author_registered", content=f"New Author Registered: {form.cleaned_data.get('name')}")
            rc.save()

        return render(request, 'home/addauth.html', {'form': form})

    else:
        messages.info(request, 'Enter the Admin Credentials to view Admin Panel!')
        return redirect('signin')


def viewsub(request):
    if request.user.is_authenticated and request.user.is_superuser:
        subs = Subject.objects.all()
        return render(request, 'home/vsubs.html', {'subs': subs})

    else:
        messages.info(request, 'Enter the Admin Credentials to view Admin Panel!')
        return redirect('signin')

def viewbooks(request):
    if request.user.is_authenticated and request.user.is_superuser:
        subjects = Subject.objects.all()
        books = BookDetail.objects.all()
        return render(request, 'home/vbooks1.html', {'books': books, 'sub': subjects})

    else:
        messages.info(request, 'Enter the Admin Credentials to view Admin Panel!')
        return redirect('signin')

def viewsubbooks(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        s = Subject.objects.get(id=id)

        books = BookDetail.objects.filter(sub=s)

        return render(request, 'home/vbooks.html', {'books': books})

    else:
        messages.info(request, 'Enter the Admin Credentials to view Admin Panel!')
        return redirect('signin')


def viewauth(request):
    if request.user.is_authenticated and request.user.is_superuser:
        author = Author.objects.all()
        return render(request, 'home/vauth.html', {'auth': author})

    else:
        messages.info(request, 'Enter the Admin Credentials to view Admin Panel!')
        return redirect('signin')

def delbook(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        b = BookDetail.objects.get(id=id)
        books = BookDetail.objects.all()
        cur_sub = b.sub
        s = Subject.objects.get(sub = cur_sub)

        auth = ','.join([author.name for author in b.author.all()])

        if request.method == "POST":
            messages.info(request, f"Book {b.title} by {auth} has been deleted!")
            b.delete()
            return redirect('viewsubbooks', s.id)

        return render(request, 'home/vbooks.html', {'books': books})

    else:
        messages.info(request, 'Enter the Admin Credentials to view Admin Panel!')
        return redirect('signin')

def delsub(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        sub = Subject.objects.get(id=id)
        subs = Subject.objects.all()
        if request.method == "POST":
            messages.info(request, f'Subject {sub.sub} has been deleted!')
            sub.delete()
            return redirect('viewsub')
        return render(request, 'home/vsubs.html', {'subs': subs})

    else:
        messages.info(request, 'Enter the Admin Credentials to view Admin Panel!')
        return redirect('signin')

def delauth(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        aut = Author.objects.get(id=id)
        auth = Author.objects.all()
        if request.method == "POST":
            messages.info(request, f'Author {aut.name} for Subject: {aut.sub} has been deleted!')
            aut.delete()
            return redirect('viewauth')

        return render(request, 'home/vauth.html', {'auth': auth})

    else:
        messages.info(request, 'Enter the Admin Credentials to view Admin Panel!')
        return redirect('signin')

def editsubs(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        sub = Subject.objects.get(id=id)
        old_sub = sub.sub
        if request.method == "POST":
            form = SubForm(request.POST, instance=sub)
            if form.is_valid():
                form.save()
                messages.info(request, f'Subject {old_sub} has been updated to {sub.sub}!')
                return redirect('viewsub')
        else:
            form = SubForm(instance=sub)

        return render(request, 'home/editsub.html', {'form': form, "old_sub": old_sub})

    else:
        messages.info(request, 'Enter the Admin Credentials to view Admin Panel!')
        return redirect('signin')


def editauth(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        auth = Author.objects.get(id=id)
        old_sub = auth.sub
        old_name = auth.name

        if request.method=="POST":
            form = AuthForm(request.POST, instance=auth)
            if form.is_valid():
                form.save()
                return redirect('viewauth')
        else:
            form = AuthForm(instance=auth)

        return render(request, 'home/editauth.html', {'form': form, "old_sub": old_sub, "old_name": old_name})

    else:
        messages.info(request, 'Enter the Admin Credentials to view Admin Panel!')
        return redirect('signin')



def editbook(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        book = BookDetail.objects.get(id=id)
        cur_det = {'bname': book.title,
         'bauth': ','.join([author.name for author in book.author.all()]),
         'bsub': book.sub}

        s = Subject.objects.get(sub = book.sub)

        if request.method == "POST":
            form = BookForm(request.POST, request.FILES, instance=book)
            if form.is_valid():
                form.save()
                messages.info(request, f'Book {book.title} has updated!')
                return redirect('viewsubbooks', s.id)

        else:
            form = BookForm(instance=book)
        return render(request, 'home/editbook.html', {'form': form, 'cur_det': cur_det})

    else:
        messages.info(request, 'Enter the Admin Credentials to view Admin Panel!')
        return redirect('signin')


def bookreq(request):
    if request.user.is_authenticated and request.user.is_superuser:
        approvals = BookIssueApproval.objects.filter(approve = 'Not viewed')


        return render(request, 'home/userrequests.html', {'app':approvals})

    else:
        messages.info(request, 'Enter the Admin Credentials to view Admin Panel!')
        return redirect('signin')


def reqapp(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        app = BookIssueApproval.objects.get(id=id)
        app.approve = "Approve"
        app.save()


        br1 = Borrower.objects.create(
            bdate = datetime.today(),
            book = app.bookn,
            bwr = app.issuer,
            sub = app.sub,
            img = app.coverp
        )
        br1.save()

        rc = RecentAct.objects.create(cat="user_borrow_book", content=f"{br1.bwr} borrowed the book {br1.book}")
        rc.save()


        user1 = get_object_or_404(User, username=str(app.issuer))


        subject = f'Book issue request - approved!'
        message = f'''
Dear {app.issuer},\n\nI hope this message finds you well.\n\nI am writing to inform you that my request for the book titled {app.bookn} has been approved.
Expected Return Date: {br1.rdate.date()}
Kindly proceed with the necessary steps for the issuance or 
let me know if any further information is required from my end.\n\nThank you for your support and assistance.\n\nBest regards,\nAdmin\nLMS+
'''
        recipient = [user1.email]

        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient, fail_silently=True)


        return redirect('userrequests')

    else:
        messages.info(request, 'Enter the Admin Credentials to view Admin Panel!')
        return redirect('signin')


def reqdec(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        app = BookIssueApproval.objects.get(id=id)
        app.approve = "Decline"
        app.save()
        user1 = get_object_or_404(User, username=str(app.issuer))


        subject = f'Book issue request - denied!'
        message = f'''Dear {app.issuer},

I hope you are doing well.

I regret to inform you that your request to issue the book titled {app.bookn} has not been approved at this time. This may be due to availability constraints, borrowing limits, or other policy-related reasons.

If you have any questions or would like further clarification, please feel free to reach out.

Thank you for your understanding.

Best regards,\n\Admin\nLMS+
'''



        recipient = [user1.email]

        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient, fail_silently=True)

        return redirect('userrequests')

    else:
        messages.info(request, 'Enter the Admin Credentials to view Admin Panel!')
        return redirect('signin')




def trackusers(request):
    if request.user.is_authenticated and request.user.is_superuser:
        bwr = Borrower.objects.all()
        for i in bwr:
            if (i.rdate < datetime.today().date()) and (i.status != 'Returned'):
                i.status = "Due"
                i.save()



        return render(request, 'home/useracti.html', {'bwrs': bwr})

    else:
        messages.info(request, 'Enter the Admin Credentials to view Admin Panel!')
        return redirect('signin')

def search_result(request):
    if request.method == "POST":
        search_val = request.POST['sbn']
        books = BookDetail.objects.filter(title__contains = search_val)

    return render(request, 'home/search.html', {'books': books, 'search':search_val})
