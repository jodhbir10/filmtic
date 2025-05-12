from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully! You can now Log in!')
            return redirect('app-login')
        else:
            messages.error(request, f'Form is not valid, please follow the rules!')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html',{'form':form})


