from django.shortcuts import render, redirect, get_object_or_404
from .models import Hospital
from .forms import HospitalForm
from django.contrib import messages
from django.db.models import Q


# Create your views here.

# CREATE
def home(request):
    form = HospitalForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, f'Created [{form.patient}] Succesfully 😊')
        return redirect('patient_list')
    return render(request, 'home.html', {'form':form})


# READ
def patient_list(request):
    search = request.GET.get('browse')

    if search:
        data = Hospital.objects.filter(
            Q(doctor__icontains = search) |
            Q(patient__icontains = search) |
            Q(disease__icontains = search) |
            Q(age__icontains = search) |
            Q(gender__icontains = search) |
            Q(phno__icontains = search) 
        )
    else:
        data = Hospital.objects.all()
    return render(request, 'patient_list.html', {'data':data, 'search':search})

# UPDATE
def update_patient(request, pk):
    data = get_object_or_404(Hospital, id=pk)
    form = HospitalForm(request.POST or None, request.FILES or None, instance=data)

    if form.is_valid():
        form.save()
        messages.success(request, f'Updated [{data.patient}] Succesfully 🫡')
        return redirect('patient_list')
    return render(request, 'update_patient.html', {'form':form})

# DELETE
def delete_patient(request, pk):
    data = get_object_or_404(Hospital, id=pk)
    if request.method == 'POST':
        data.delete()
        messages.success(request, f'Deleted [{data.patient}] Succesfully 🥺')
        return redirect('patient_list')
    return render(request, 'delete_patient.html', {'data':data})


# ==============================================================================================================================

# AUTHENTICATION
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User     # User is a model

# AUTHORISATION
from django.contrib.auth.decorators import login_required

# signup, signin, profile, update_profile, update_password
def signup(request):
    if request.method == 'POST':
        User.objects.create_user(            # instead of create  we use create_user
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            username = request.POST['username'],
            password = request.POST['password']
        )
        messages.success(request, 'User Registered Succesfully! 🫡')
        return redirect('signin')
    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        user = authenticate(request,
                                   username = request.POST['username'],
                                   password = request.POST['password'] 
                                   )
        if user:
            login(request, user)
            messages.success(request, 'Logged in Successfully 😊')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid credentials! 🥺')
            return redirect('signin')
    return render(request, 'signin.html')

@login_required(login_url='signin')
def profile(request):
    return render(request, 'profile.html', {'chethan':request.user})


@login_required(login_url='signin')
def update_profile(request):
    data = request.user # extracted the currently active profile
    if request.method == 'POST':
        data.first_name = request.POST['first_name']
        data.last_name = request.POST['last_name']
        data.email = request.POST['email']
        data.username = request.POST['username']
        data.save()
        messages.success(request, 'Profile Updated Succesfully! 🫡')
        return redirect('profile')
    return render(request, 'update_profile.html', {'data':data})

@login_required(login_url='signin')
def update_password(request):
    data = request.user
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if not data.check_password(old_password):
            messages.warning(request, 'Old Password is incorrect !')
        elif new_password != old_password:
            messages.warning(request, 'Password does not match !')
        else:
            data.set_password(new_password)
            data.save()
            update_session_auth_hash(request,data)
            messages.warning(request, 'Password Updated Successfully !')
            return redirect('update_password')
    return render(request, 'update_password.html', {'data':data})

@login_required(login_url='signin')
def signout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('signin')
