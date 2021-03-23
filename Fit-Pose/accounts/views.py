from django.shortcuts import render

# Create your views here.


#----------------------------- HOME ------------------------------------#

def home(request):
    return render(request, 'accounts/home.html')


#----------------------------- LOGIN ------------------------------------#

def login(request):
    return render(request, 'accounts/login.html')



#----------------------------- REGISTER ------------------------------------#

def signup(request):
    return render(request, 'accounts/signup.html')

#----------------------------- LOGOUT ------------------------------------#

def logout(request):
    return render(request, 'accounts/signup.html')