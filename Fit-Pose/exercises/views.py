from django.shortcuts import render

# Create your views here.


#----------------------------- EXERCISE LIST ------------------------------------#

def exercises(request):
    return render(request, 'exercises/allexercises.html')