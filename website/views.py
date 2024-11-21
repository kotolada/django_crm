from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

def home(request):
    # Grab everything and assign it to the variable
    records = Record.objects.all
    # Check to see if logging in
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.error(request, "There was an error logging in, please try again")
            return render(request, 'home.html', {})
    else:
        return render(request, 'home.html', {'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        # ^ A new form instance is created and populated
        # with the info the user submitted (request.Post)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered!')
            return redirect('home')
    # If the user haven't submitted (POSTed) data yet,
    # show them the registration form
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    # If the form is not valid, re-render the form along with
    # user input and error messages.
    return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look Up Records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.error(request, 'You must be logged in to view that page.')
        return redirect(request, 'home.html')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record has been deleted.")
        return redirect('home')
    else:
        messages.error('You must be logged in to do that.')
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, 'Record added.')
                return redirect('home')
        return render(request, "add_record.html", {'form': form})
    else:
        messages.error('You must be logged in to do that.')
        return redirect('home')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        # Add instance to propagate the form with
        # the existing information.
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record has been updated.')
            return redirect('home')
        return render(request, "update_record.html", {'form': form})
    else:
        messages.error('You must be logged in to do that.')
        return redirect('home')


    