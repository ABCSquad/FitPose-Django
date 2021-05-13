from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileUpdateForm
from main.models import Session, Stats
from exercises.models import Exercise

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
    sessions = {}
    datetime = get_data(request, sessions)
    cf_per = compute_progress(sessions)
    return render(request, 'accounts/dashboard.html', {'datetime':datetime, 'cf_per':cf_per})

# For getting data of the user's previous workouts
def get_data(request, sessions):
    session_ids = [session['id'] for session in list(Session.objects.filter(user=request.user).values('id'))]
    datetime = []
    limit = 0 # For setting the no. of sessions to save
    for i in reversed(session_ids):
        stats_obj = Stats.objects.filter(session=i)
        if stats_obj and limit < 14:
            dt = getattr(get_object_or_404(Session, pk=i), 'datetime')
            dt = f'{dt.strftime("%b")} {dt.day}, {dt.hour}:{dt.minute}'
            datetime.append(dt)
            sessions[i]= [stats_obj]
            limit += 1
    datetime.reverse()
    return datetime

# For computing progress in the last few sessions
def compute_progress(sessions):
    cf_per, cf, wf = [], [], [] 
    for i, session in enumerate(sessions.keys()):
        cf.append(0) # Correct form in seconds for each rep
        wf.append(0) # Wrong form in seconds for each rep
        for stats in sessions[session].pop():
            cf[i] += float(getattr(stats, 'correct_form'))
            wf[i] += float(getattr(stats, 'wrong_form'))
        percentage = round(cf[i]/(cf[i]+wf[i])*100, 1)
        cf_per.append(percentage) # Percentage of exercise performed in correct form for each session
    cf_per.reverse()
    return cf_per

#-----------------------------SESSIONS------------------------------------#
def session(request):
    user_id = request.user.id
    all_sessions = Session.objects.filter(user_id=user_id)
    max_reps, sessions, ex_name = get_sessions(all_sessions)
    return render(request, 'accounts/session.html', {"data": zip(sessions, max_reps, ex_name)})

# For saving non-null sessions and getting max reps performed in said sessions
def get_sessions(all_sessions):
    sessions = []
    rep_no = []
    ex_name = []
    for session in all_sessions:
        stats = Stats.objects.filter(session_id=session.pk).last()
        if stats is not None:
            sessions.append(session)
            max_reps = int(getattr(stats, 'rep_no'))
            rep_no.append(max_reps)
            ex_id = getattr(session, 'exercise_id')
            exercise = getattr(get_object_or_404(Exercise, pk=ex_id), 'title')
            ex_name.append(exercise)
    sessions.reverse()
    rep_no.reverse()
    ex_name.reverse()
    return rep_no, sessions, ex_name

