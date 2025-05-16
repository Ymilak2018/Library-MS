import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from USERS.models import Borrower
from Books.models import Subject, BookDetail, BookIssueApproval, RecentAct
from .models import Borrower, Profile
from django.contrib.auth.models import User
from .forms import EditUserForm
from LMS.home_forms import SignupForm


# Create your views here.

@login_required(login_url='signin')
def userdb(request):
    if request.user.is_authenticated:

        usern = request.user.username
        bwrs = Borrower.objects.filter(bwr=usern, status__in=['Not Returned', 'Due'])
        due_bwrs = Borrower.objects.filter(bwr=usern, status = 'Due')
        returned_books = Borrower.objects.filter(bwr=usern, status = 'Returned')
        cxt = {
            'total_books_borrowed': len(bwrs),
            'due_books': len(due_bwrs),
            'returned_books': len(returned_books),
            'bwrs': bwrs
        }

        return render(request, 'home/userdb.html', cxt)
    else:
        return redirect('signin')


def listedsubs(request):

    subjects = Subject.objects.all()
    books = BookDetail.objects.all()
    return render(request, 'user_templates/listedsubs.html', {'books': books, 'sub': subjects})

def listedbooks(request, id):

    s = Subject.objects.get(id=id)

    books = BookDetail.objects.filter(sub=s)

    return render(request, 'user_templates/listedbooks.html', {'books': books})

def bookissueform(request, id):

    bookdetail1 = BookDetail.objects.get(id=id)

    if request.method == "POST":
        BookIssueApproval.objects.create(coverp = bookdetail1.coverp, bookn = bookdetail1.title, isstime = datetime.datetime.today(), issuer = request.user.username, sub=bookdetail1.sub)

        messages.info(request, 'Request Initiated , wait for the approval from Admin!')
        return redirect('userdb')


    return render(request, 'user_templates/bookissue.html', {'book': bookdetail1})

def returnbooks(request):

    usern = request.user.username
    bwrs = Borrower.objects.filter(bwr=usern, status__in=['Not Returned', 'Due'])

    return render(request, 'user_templates/returnbooks.html', {'bwrs': bwrs})


def returnbooks1(request, id):

    bwr = Borrower.objects.get(id=id)
    bwr.status = "Returned"
    bwr.save()

    rc = RecentAct.objects.create(cat="user_borrow_book", content=f"{bwr.bwr} returned the book {bwr.book}")
    rc.save()

    return redirect("returnbooks")

def editprofile(request, id):

    user1 = User.objects.get(id=id)
    pro1 = Profile.objects.get(user = user1)
    if request.method == "POST":
        form = EditUserForm(request.POST)

        if form.is_valid():

            user1.username = form.cleaned_data.get('username')
            user1.email = form.cleaned_data.get('email')
            user1.save()
            pro1.user = user1
            pro1.role = form.cleaned_data.get('role')
            pro1.save()
            messages.info(request, f"User details have been updated for {user1.username}")
            return redirect("profile")
    else:
        form = EditUserForm()


    return render(request, 'user_templates/editprofile.html', {'form': form, 'pro': pro1, 'user': user1})
