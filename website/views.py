from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from django.db.models import Q


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # records = Record.objects.all()
    records = Record.objects.filter(
        Q(first_name__icontains=q) | 
        Q(last_name__icontains=q)
    )

    # check to see if logging in
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "There Was An Error Loggin In, Please Try Again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})


@login_required(login_url='home')
def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            # authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You Have Successfully Registered! Welcome!")
                return redirect('home')
        
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


@login_required(login_url='home')
def customer_record(request, pk):
    record = get_object_or_404(Record, id=pk)
    return render(request, 'record.html', {'record': record})


@login_required(login_url='home')
def delete_record(request, pk):
    record = get_object_or_404(Record, id=pk)
    record.delete()
    messages.success(request, "Record Deleted Successfully!!!")
    return redirect('home')


@login_required(login_url='home')
def add_record(request):
    form = AddRecordForm(request.POST or None)

    if request.method == 'POST':
        form = AddRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Added...")
            return redirect('home')


    return render(request, 'add_record.html', {'form': form})


@login_required(login_url='home')
def update_record(request, pk):
    current_record = Record.objects.get(id=pk)
    form = AddRecordForm(request.POST or None, instance=current_record)
    if form.is_valid():
        form.save()
        messages.success(request, "Record has been updated!")
        return redirect('home')

    return render(request, 'update_record.html', {'form': form})
