from multiprocessing import context
from django.shortcuts import render, redirect
from queues.models import Queue
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import UserProfile
from .forms import UserRegistrationForm, UserProfileForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            messages.success(request, 'Registration successful! Please complete your profile.')
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')

    else:
        return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now log out')
        return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    hardwareCount = Queue.objects.filter(type__contains='hardware').count()
    softwareCount = Queue.objects.filter(type__contains='software').count()
    phoneCount = Queue.objects.filter(type__contains='phone').count()
    accountCount = Queue.objects.filter(type__contains='other').count()

    # Get filter parameters from request
    technician = request.GET.get('technician', '')
    status = request.GET.get('status', '')
    type_filter = request.GET.get('type', '')

    # Build base query
    base_query = (
        Q(technician__istartswith='Not Assigned') | 
        Q(status='In Progress') |
        Q(status='Done')
    )

    # Special handling for "My Tickets" filter
    if technician == request.user.username or technician == request.user.first_name:
        base_query &= Q(technician__icontains=request.user.first_name)
    elif technician:  # For other technician filters
        base_query &= Q(technician__icontains=technician)

    # Add other filters if provided
    if status:
        base_query &= Q(status__icontains=status)
    if type_filter:
        base_query &= Q(type__icontains=type_filter)

    queueLists = Queue.objects.filter(base_query).values()
    
    context = {
        'queueLists': queueLists,
        'hardwareCount': hardwareCount,
        'softwareCount': softwareCount,
        'phoneCount': phoneCount,
        'accountCount': accountCount,
        'profile': request.user.profile,
        'technician': technician,
        'status': status,
        'type': type_filter
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('dashboard')
    else:
        profile_form = UserProfileForm(instance=profile)
    
    return render(request, 'accounts/profile.html', {
        'profile_form': profile_form,
        'profile': profile
    })

    
