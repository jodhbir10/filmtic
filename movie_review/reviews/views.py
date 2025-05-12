from django.shortcuts import render
from . import views
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'reviews/index.html')

@login_required
def dashboard(request):
    return render(request, 'reviews/dashboard.html')



