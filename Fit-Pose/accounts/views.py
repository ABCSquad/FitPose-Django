from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileUpdateForm

# Create your views here.


#----------------------------- HOME ------------------------------------#

def home(request):
    return render(request, 'accounts/home.html')


#----------------------------- LOGIN ------------------------------------#

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(
            username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'accounts/login.html')
   



#----------------------------- REGISTER ------------------------------------#

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                print("Username taken")
                return render(request, 'accounts/signup.html',{'error':'Username already exists'})
            elif User.objects.filter(email=email).exists():
                print("Email taken")
                return render(request, 'accounts/signup.html',{'error':'Email has been taken'})
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                print("User creation successful")
        else:
            print("Passwords don't match")
            return render(request, 'accounts/signup.html', {'error': 'Passwords must match'})
        return redirect("login")
    else:
        return render(request,'accounts/signup.html')
    
    

#----------------------------- LOGOUT ------------------------------------#

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
  

#----------------------------- PROFILE ------------------------------------#
@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        p_form = ProfileUpdateForm(instance=request.user.profile) 
        context ={
            'p_form':p_form
        }

    return render(request, 'accounts/profile.html', context)


#-----------------------------DASHBOARD ------------------------------------#
@login_required
def dash(request):
    return render(request, 'accounts/dashboard.html')