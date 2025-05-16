from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .home_forms import SigninForm, SignupForm, EditProForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Books.models import Subject, BookDetail, BookIssueApproval, RecentAct
from USERS.models import Profile, Borrower
import re
from USERS.forms import EditUserForm
from django.conf import settings
from django.core.mail import send_mail, EmailMessage




def signin(request):

    if "user_id" in request.session:

        if request.user.is_superuser:
            return redirect('homeadmin')
        else:
            return redirect('userdb')

    else:

        form = SigninForm()

        if request.method == 'POST':
            form = SigninForm(request.POST)
            usern = request.POST.get('username')
            passw = request.POST.get('password')
            lid = re.findall('^(?:LID|STU|FAC|STA)000.*', usern)

            if len(lid) > 0 :
                pro = get_object_or_404(Profile, libid = usern)
                pro_user = pro.user.username
                user = authenticate(request, username = pro_user, password = passw)
            else:
                user = authenticate(request, username = usern, password = passw)


            if user is not None:
                request.session['user_id'] = user.id

                messages.success(request, 'Logged In Successfully!!')

                login(request, user)


                if request.user.is_superuser:
                    return redirect('homeadmin')
                else:
                    return redirect('userdb')
            else:
                messages.error(request, 'Bad Credentials, try again!')
                return redirect('signin')


        return render(request, 'home/signin.html', {'form': form})


def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

            role = request.POST.get('role')
            newuser = User.objects.order_by('-id').first()
            lid = role[:3].upper() + '000' + str(newuser.id)

            profile1 = Profile.objects.create(user = newuser, role = role, libid = lid)

            messages.success(request, 'You are now registered and your profile has been created successfully, Sign In!!')
            messages.info(request, f'Check mail for your details')

            rc = RecentAct.objects.create(cat = 'new_user_registered', content = f"New User registered: {form.cleaned_data.get('username')}")
            rc.save()


            l = (len(form.cleaned_data.get('password1'))-3) * '*'
            p = l + form.cleaned_data.get('password1')[-3:]
            subject = 'Registration Successful in QB LMS'
            message = f" Thank you for registering with QB LMS. \n Your Username : {form.cleaned_data.get('username')} \n Your Library ID : {profile1.libid} \n  Your Password : {p} \n Your Role : {role} \n\n Happy Reading!!"
            recipient = [form.cleaned_data.get('email')]


            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient, fail_silently=True)


            return redirect('signin')


    return render(request, 'home/signup.html', {'form': form})

@login_required(login_url='signin')
def homeadmin(request):

    bwr = len(Borrower.objects.all())
    pro = len(Profile.objects.all())
    bd = len(BookDetail.objects.all())
    rcs = RecentAct.objects.all().order_by('-created_at')[:7]

    cxt = {
        'rcs': rcs,
        'bwr': bwr,
        'pro': pro,
        'bd': bd
    }
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'home/lms.html', cxt)
    else:
        messages.info(request, 'Only Admins have the access of the Admin Panel!!')
        return redirect('signin')



def profile(request):
    user = get_object_or_404(User, username=request.user.username)
    profile = Profile.objects.get(user = user)

    if request.user.is_superuser:
        return render(request, 'home/profile.html', {'user': user, 'profile': profile})
    else:
        return render(request, 'home/profile1.html', {'user': user, 'profile': profile})

def viewusers(request):
    if request.user.is_authenticated and request.user.is_superuser:
        users = User.objects.all()

        return render(request, 'home/vusers.html', {'users': users})
    else:
        messages.info(request, 'Enter the Admin Credentials to view Admin Panel!')
        return redirect('signin')


def deluser(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        user = get_object_or_404(User, id=id)
        users = User.objects.all()
        if request.method == "POST":
            messages.info(request, f'User {user.username} has been deleted!')
            user.delete()
            return redirect('viewusers')
        return render(request, 'home/vusers.html', {'users': users})
    else:
        messages.info(request, 'Enter the Admin Credentials to view Admin Panel!')
        return redirect('signin')



def editpro(request):
    if request.user.is_superuser and request.user.is_authenticated:
        user1 = User.objects.get(id = request.user.id)
        pro1 = Profile.objects.get(user = user1)

        if request.method == "POST":
            form = EditProForm(request.POST)

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
            form = EditProForm()

        return render(request, 'home/edituser.html', {'form': form, "user": user1, 'pro': pro1})



def signout(request):

    logout(request)

    return redirect('start')

def start(request):
    return render(request, 'home/start.html')