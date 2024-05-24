from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .filters import *
from .models import *
from .forms import *


def homepage1(request):
    if request.user.is_authenticated:
        user = request.user
        if hasattr(user, 'profile'):
            profile = user.profile
            return HttpResponse('you are a perosnal profile')
        elif hasattr(user, 'organizationprofile'):
            organization_profile = user.organizationprofile
            return HttpResponse('you are a organization profile')
        else:
            return HttpResponse('error')

    else:
        # Redirect to a login page or handle anonymous users
        return HttpResponse('Please log in to view this page.')
# def homepage(request):
#     posts = OrganizationProfile.objects.all()
#     f = PostFilter(request.GET , queryset=posts)
#     organizations = f.qs
#     context={
#         'organizations':organizations
#     }
#     return render(request,'home.html',context)

def homepage(request):
    search_query = request.GET.get('search')
    posts = OrganizationProfile.objects.all()
    if search_query:
        posts = posts.filter(name__icontains=search_query) 
    f = PostFilter(request.GET, queryset=posts)
    organizations = f.qs
    context = {'organizations': organizations}
    return render(request, 'home.html', context)
def accountSettings(request):
    user = request.user
    profile = None
    org_profile = None
    form_class = None
    instance = None

    # Attempt to retrieve profile based on user type
    try:
        profile = Profile.objects.get(user=user)
        form_class = MemberForm
        instance = profile
    except Profile.DoesNotExist:
        pass

    try:
        org_profile = OrganizationProfile.objects.get(user=user)
        form_class = OrganizationForm
        instance = org_profile
    except OrganizationProfile.DoesNotExist:
        pass

    if not profile and not org_profile:
        return HttpResponse('You need to create a profile.')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = form_class(instance=instance)
        # Add user's username to the form
        form.fields['username'].initial = user.username  # Assuming 'username' is a field in your form

    context = {'form': form}
    return render(request, 'account_setting.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password incorrect')

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            print("validated")
            user = form.save()
            login(request, user)  
            return redirect('home')  
        else:
            return HttpResponse('failed')
    else:
        
        form = CreateUserForm()
        print(form.errors)
    return render(request, 'dummy.html', {'form': form})

def logoutPage(request):
    logout(request)
    return redirect('login')

def explore(request,id):
    try:
        organization = OrganizationProfile.objects.get(id=id)
      
        context={
            'organization':organization
        }
        if request.GET.get('send'):
            
            if request.user is not None:
                print(organization.contact_email)
                subject = 'subj'
                message = "This is my message"
                sender = settings.EMAIL_HOST_USER
                to = ['dipeshacharya87@gmail.com',]

                send_mail(subject, message, sender, to)
        return render(request , 'register.html',context)
    except:
        return HttpResponse("error")
  

